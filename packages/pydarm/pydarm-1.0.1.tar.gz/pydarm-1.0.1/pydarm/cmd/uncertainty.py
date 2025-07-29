import os
from datetime import timedelta, timezone

import gpstime
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict as tsd
import numpy as np

from .. import __version__
from ._log import logger, log_to_file, CMDError
from . import _args
from ._const import (
    IFO,
    set_cal_data_root,
    DEFAULT_UNCERTAINTY_CONFIG_PATH,
    CAL_UNCERTAINTY_ROOT,
)
from ._git import check_report_git_status
from ._util import write_pydarm_version
from ._report import Report, list_reports
from ._uncertainty import Uncertainty
from ..uncertainty import DARMUncertainty
from ._influx import CalInfluxFetcher


# span of TDCF data used for model uncertainty
# FIXME: this has to match how pydarm parses this all internally
TDCF_SPAN = 130

# span of TDCF data used for model uncertainty
MONITOR_SPAN = 3600

# offset from the current time for default time calculation,
# NOTE: needs to be more than half the monitor span
OFFSET_FROM_NOW = MONITOR_SPAN/2 + 360

# default number of trials
DEFAULT_TRIALS = 1000

# default magnitude range (-DEFAULT_MAG_LIM, DEFAULT_MAG_LIM) percent
DEFAULT_MAG_LIM = 10

# default phase range (-DEFAULT_PHA_LIM, DEFAULT_PHA_LIM) deg
DEFAULT_PHA_LIM = 10

# default frequency array for calc
# FIXME: should this pull from the GPR?  or be specified in config?
DEFAULT_FREQ_ARRAY = '10:100:4999'


def fetch_monitor_line_data(fetcher, gps_start, gps_end):
    """fetch monitoring line data from the InfluxDB"""
    meas = ['TF_phase', 'TF_mag', 'coherence', 'line_onoff']
    fields = ['time', 'data', 'oscillator_frequency', 'strain_channel', 'lock_state']
    conditions = [''' "hoft_ok" = 'HOFT_OK' AND "obs_intent" = 'OBS_INTENT'
                  AND "line_on" = 'on' AND "coh_threshold" = 'cohok' ''']
    df = fetcher.fetch_data(gps_start, gps_end, meas, fields, conditions=conditions)
    # by default mag saved with dtype=object
    df['TF_mag'] = df.TF_mag.astype(float)
    data = df[['time', 'oscillator_frequency', 'TF_phase', 'TF_mag', 'coherence', 'line_onoff']]
    data.sort_values(by=['oscillator_frequency'], ascending=True, inplace=True)
    return data


def add_args(parser):
    parser.add_argument(
        'time', metavar='DATETIME', nargs='?',
        help=f"time to calculate uncertainty, defaults to now-{OFFSET_FROM_NOW} seconds")
    _args.add_report_option(parser, default=None)
    parser.add_argument(
        '--uncertainty-config', '-u', metavar='INI', default=DEFAULT_UNCERTAINTY_CONFIG_PATH,
        help=f"uncertainty config INI file (default: {DEFAULT_UNCERTAINTY_CONFIG_PATH})")
    parser.add_argument(
        '--scald-config', metavar='YAML',
        help="InfluxDB client config for incorporating monitor line data")
    parser.add_argument(
        '--outdir', '-o', metavar='DIR',
        help="write uncertainty to specified directory")
    _args.add_freqspec_option(parser, default=DEFAULT_FREQ_ARRAY)
    parser.add_argument(
        '--trials', '-t', metavar='N', type=int, default=DEFAULT_TRIALS,
        help=f"override default number of trials (default: {DEFAULT_TRIALS})")
    parser.add_argument(
        '--correction-tf', '-c', metavar='TXT',
        help="Multiply sampled responses by a correction transfer function (the TXT file needs \
        to be a three-column CSV with frequency, magnitude, and phase; the frequency vector must \
        be the same as the specified frequency array.)")
    parser.add_argument(
        '--seed', '-s', metavar='N', type=int, default=None,
        help="specify a random generator seed value for reproducability")


def main(args):
    """generate calibration uncertainty budget

    This command calculates the frequency-dependent calibration
    uncertainty budget at the specified time.  Measurement MCMC and
    GPR output is pulled from the report directory, and pipeline TDCFs
    are pulled from NDS.

    The primary input is a pydarm cmd "report" that includes the
    relevant model INI file, and the measurement MCMC and GPR
    calculations used to calculate the uncertainty.  If no report is
    specified the last available valid report before the specified
    time will be used.  The configuration parameters for the
    uncertainty calculation itself are pulled from the local `ifo`
    repo.

    This command outputs the frequency-domain uncertainty arrays and
    bode plots of the amplitude and phase uncertainty to the output
    directory.  If an output directory is not specified the output
    will be written to a GPS-specific directory in the
    CAL_UNCERTAINTY_ROOT.

    """
    logger.info(f"pydarm version {__version__}")

    if not args.time:
        gt = gpstime.parse('now') - timedelta(seconds=OFFSET_FROM_NOW)
    else:
        gt = gpstime.parse(args.time)

    gps = int(gt.gps())

    logger.info(f"time to evaluate uncertainty: {gt} (GPS {gps})")

    tdcf_gps_start = gps - TDCF_SPAN/2
    tdcf_gps_end = gps + TDCF_SPAN/2

    if args.scald_config:
        logger.info("configuring InfluxDB fetcher for monitor line data...")
        scald_fetcher = CalInfluxFetcher(args.scald_config, IFO)

        monitor_gps_start = gps - MONITOR_SPAN/2
        monitor_gps_end = gps + MONITOR_SPAN/2

        if monitor_gps_end > gpstime.parse('now').gps():
            raise CMDError(f"evaluation time too recent for monitor line incorporation, must be >{MONITOR_SPAN/2} sec in the past")  # noqa E501

    try:
        NDSSERVER = os.getenv('NDSSERVER')
        if not NDSSERVER:
            raise CMDError("NDSSERVER env var not defined.")
        host_port = NDSSERVER.split(',')[0].split(':')
        if len(host_port) > 1:
            host, port = host_port
        else:
            host = host_port[0]
            port = 31200
        logger.info(f"NDS server: {host}:{port}")
    except Exception:
        raise CMDError(f"could not parse NDSSERVER env var: {NDSSERVER}")

    state_channel = f'{IFO}:GDS-CALIB_STATE_VECTOR'
    try:
        if host == 'file':
            state = tsd.read(port)[state_channel]
        else:
            state = TimeSeries.get(state_channel, tdcf_gps_start, tdcf_gps_end)
    except Exception:
        raise CMDError("could not get IFO state")
    # If state value is even, hoft not ok, see T1900007; check start and end times
    if state.value[0] % 2 == 0 or state.value[-1] % 2 == 0:
        raise CMDError(f"hoft not ok around GPS time: {gps}")

    ########################################
    # report/config setup

    # if a report is specified we just use that report.  if none is
    # specified (the default) we find the report closest to the time
    # (see below)
    if args.report:
        report = Report.find(args.report)

    else:
        # find the last report before the time in question
        # loop over reports in reverse chronological order
        logger.info("searching for last valid report before time...")
        for report in list_reports():
            if report.id_gpstime() <= gt:
                break
        else:
            raise CMDError(f"Could not find valid exported report before time {gps}.")

    logger.info(f"report found: {report.path}")

    # check that the report git repo is clean
    check_report_git_status(report, check_valid=True)

    logger.info(f"report directory: {report.path}")
    logger.info(f"model file: {report.model_file}")

    logger.info(f"uncertainty config: {args.uncertainty_config}")
    if not os.path.exists(args.uncertainty_config):
        raise CMDError("uncertainty config file not found.")

    if args.outdir:
        output_dir = args.outdir
    else:
        gpss = str(gps)
        # split event paths into 1000000 second / 11.6 day epochs
        epoch, esecs = gpss[:-6], gpss[-6:]
        output_dir = os.path.join(
            CAL_UNCERTAINTY_ROOT,
            epoch, esecs,
        )
    logger.info(f"output directory: {output_dir}")

    out_file_base = os.path.join(
        output_dir,
        f'calibration_uncertainty_{IFO}_{gps}',
    )

    logger.info(f"using logarithmic frequency array: {args.freq}")
    freq = _args.freq_from_spec(args.freq)

    correction_tf = None
    if args.correction_tf:
        logger.info(f"loading TF correction from file:: {args.correction_tf}")
        tf = np.loadtxt(args.correction_tf)
        tf_freq = tf[:, 0]
        if (tf_freq != freq).any():
            raise CMDError("Frequency array in the correction TF does not match input freq.")
        tf_mag = tf[:, 1]
        tf_phase = tf[:, 2]
        correction_tf = tf_mag * np.exp(1j * tf_phase)

    ########################################
    # reference MCMC and GPR data

    actuation_file_map = {
        'xarm': {
            'UIM': 'actuation_L1_EX',
            'PUM': 'actuation_L2_EX',
            'TST': 'actuation_L3_EX',
        },
        'yarm': {
            'UIM': 'actuation_L1_EY',
            'PUM': 'actuation_L2_EY',
            'TST': 'actuation_L3_EY',
        },
    }

    logger.info(f"loading GPR data from report {report.id}...")
    sensing_gpr_file = report.gen_path('sensing_gpr.hdf5')
    actuation_gpr_files_dict = {'xarm': {}, 'yarm': {}}
    for arm, stages in actuation_file_map.items():
        for stage, base in stages.items():
            gpr_file = report.gen_path(f'{base}_gpr.hdf5')
            if os.path.exists(gpr_file):
                actuation_gpr_files_dict[arm][stage] = gpr_file

    logger.info("finding reference (last exported) report...")
    try:
        ref_report = list_reports(
            exported_only=True,
            before=gt,
        )[0]
        logger.info(f"last exported report: {ref_report}")
    except IndexError:
        raise CMDError(f"could not find last exported report before time {gt}.")
    sensing_mcmc_file = ref_report.gen_path('sensing_mcmc_chain.hdf5')
    logger.info(f"Using last exported report's sensing mcmc chain: {sensing_mcmc_file}")
    actuation_mcmc_files_dict = {'xarm': {}, 'yarm': {}}
    for arm, stages in actuation_file_map.items():
        for stage, base in stages.items():
            mcmc_file = ref_report.gen_path(f'{base}_mcmc_chain.hdf5')
            if os.path.exists(mcmc_file):
                actuation_mcmc_files_dict[arm][stage] = mcmc_file
                logger.info("Using last exported report's actuation mcmc chain: "
                            f"{mcmc_file}")

    ########################################
    # model initialization

    # set CAL_DATA_ROOT env var for core
    set_cal_data_root()

    darm_unc = DARMUncertainty(
        ref_report.model_file,
        uncertainty_config=args.uncertainty_config,
        sensing_mcmc_file=sensing_mcmc_file,
        sensing_gpr_file=sensing_gpr_file,
        actuation_mcmc_files_dict=actuation_mcmc_files_dict,
        actuation_gpr_files_dict=actuation_gpr_files_dict,
    )

    ########################################
    # model uncertainty evaluation and plotting

    logger.info(f"fetching TDCF data for times [{tdcf_gps_start}, {tdcf_gps_end})...")

    channels = darm_unc.tdcf_channel_list()

    if host == 'file':
        data = tsd.read(port)
    else:
        data = tsd.get(  # noqa 841
            channels,
            tdcf_gps_start, tdcf_gps_end,
            host=host, port=int(port),
            verbose=True,
        )

    logger.info("evaluating model uncertainty...")

    # create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # calculate the model uncertainty
    try:
        samples = darm_unc.compute_response_uncertainty(
            gps,
            freq,
            save_to_file_txt=out_file_base+'_pydarm.txt',
            trials=args.trials,
            data=data,
            shift_sample_tf=correction_tf,
            seed=args.seed
        )

        response_mag_quant, response_pha_quant = darm_unc.response_quantiles(
            samples,
        )
    except Exception:
        # if there are any errors and we don't write out results, then
        # remove the directory so we don't have empty directories
        # lying around
        os.rmdir(output_dir)
        raise

    ##########
    # populate the uncertainty directory

    unc = Uncertainty.create(
        gps,
        report,
        args.uncertainty_config,
        output_dir
    )

    log_to_file(logger, unc.gen_path("log"))

    write_pydarm_version(unc.gen_path('pydarm_version'))

    ##########

    logger.info("plotting model uncertainty...")

    title = f"""{IFO} Calibration Error and Uncertainty
    {gt.astimezone(timezone.utc)} [GPS {gt.gps()}]"""

    fig = darm_unc.plot_response_samples(
        freq,
        response_mag_quant, response_pha_quant,
        IFO,
        y_mag=DEFAULT_MAG_LIM, y_pha=DEFAULT_PHA_LIM,
    )

    ax0, _ = fig.get_axes()
    ax0.set_title(title)

    fig.savefig(
        out_file_base+'_pydarm.png',
        bbox_inches='tight',
        pad_inches=0.2
    )

    ########################################
    # monitor uncertainty evaluation and plotting

    if args.scald_config:

        logger.info(f"fetching monitor data from Influx for times [{monitor_gps_start}, {monitor_gps_end})...")  # noqa E501

        # fetch InfluxDB measurements
        monitor_line_data = fetch_monitor_line_data(
            scald_fetcher,
            monitor_gps_start, monitor_gps_end,
        )

        logger.info("evaluating model+monitor uncertainty...")

        # compute updated (modelled + measured) response uncertainty
        response_mag_quant_mon, response_pha_quant_mon = \
            darm_unc.response_uncertainty_combine_with_mon_line_data(
                freq,
                response_mag_quant, response_pha_quant,
                monitor_line_data,
                output_dir_diagnostics=output_dir,
                save_to_file_txt=out_file_base+'.txt')

        logger.info("plotting model+monitor uncertainty...")

        fig = darm_unc.plot_response_samples(
            freq,
            response_mag_quant_mon, response_pha_quant_mon,
            IFO,
            y_mag=DEFAULT_MAG_LIM, y_pha=DEFAULT_PHA_LIM,
            monitor_line_data=monitor_line_data,
        )
        ax = fig.get_axes()
        ax[0].set_title(title)

        fig.savefig(
            out_file_base+'.png',
            bbox_inches='tight',
            pad_inches=0.2
        )

        fig = darm_unc.plot_response_samples_compare(
            freq, [], [],
            (response_mag_quant_mon, response_mag_quant),
            (response_pha_quant_mon, response_pha_quant),
            IFO,
            y_mag=DEFAULT_MAG_LIM, y_pha=DEFAULT_PHA_LIM,
            monitor_line_data=monitor_line_data,
        )

        ax = fig.get_axes()
        ax[0].set_title(title)

        fig.savefig(
            out_file_base+'_compare.png',
            bbox_inches='tight',
            pad_inches=0.2
        )

    ########################################

    logger.info(f"all uncertainty evaluated successfully: {output_dir}")
