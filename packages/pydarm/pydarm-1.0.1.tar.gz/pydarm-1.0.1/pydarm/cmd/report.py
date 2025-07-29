import os
import argparse
import subprocess
from copy import deepcopy
import json

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import ticker

from .. import __version__
from ._log import logger, log_to_file, CMDError
from . import _args
from ._util import (
    gen_config_calcs_filters_keys,
    write_pydarm_version,
)
from ._const import (
    IFO,
    set_cal_data_root,
    DEFAULT_MODEL_PATH,
    FREE_PARAM_LABEL_MAP,
    STAGE_LABEL_MAP,
    )
from ._report import Report, list_reports
from ._mset import MeasurementSet
from ._mcmc import sensing_MCMC, actuation_MCMC
from ._gpr import sensing_GPR, actuation_GPR
from ._history import sensing_history, actuation_history
from ._pcalplot import pcal_to_gds
from ..utils import (
    read_chain_from_hdf5,
    freqresp_to_mag_db_phase_str,
    tf_from_foton_zpk,
    tuple_from_foton_zp_format,
)
from ..fir import FIRFilterFileGeneration


def find_epoch_reports(epoch, new_report, previous_exported_report):
    """find all reports for the specified epoch (sensing or actuation)

    Returns the list of reports from the current epoch, as well as the
    reference report for the epoch.  `new_report` will be excluded
    from report list of epoch reports, and will be used as the reference
    if there is no previous exported report or this is the first report of
    an epoch.

    Parameters
    ----------
    epoch : `str` of 'sensing', 'actuation', or 'hfrl'
    new_report : `Report` object
    previous_exported_report : `Report` object

    Returns
    -------
    epoch_report: list of `Report` objects
    ref_report: `Report` object

    """
    assert epoch in ['sensing', 'actuation', 'hfrl']

    logger.info(f"scanning past reports for {epoch} epoch...")
    epoch_reports = []
    if epoch == 'hfrl':
        seek_tags = set(['epoch-hfrl'])
    else:
        seek_tags = set([f'epoch-{epoch}', 'epoch'])
    if not (seek_tags & set(new_report.tags)):
        for report in list_reports(before=new_report.id_gpstime()):
            if report.id == new_report.id:
                continue
            if report.id_gpstime() >= new_report.id_gpstime():
                continue
            logger.info(f"  including {report.id} {' '.join(report.tags)}")
            report.load_measurements()
            epoch_reports.append(report)
            # FIXME: should we check for diffs in the model ini,
            # since it's changed in model parameters that's what
            # really defines the epoch boundaries?
            if seek_tags & set(report.tags):
                logger.info(f"{epoch} epoch boundary at {report.id}")
                break
        else:
            logger.info("no reports in current epoch.")

    try:
        ref_report = epoch_reports[-1]
        ref_report_desc = 'first valid report in epoch'
    except IndexError:
        ref_report = new_report
        ref_report_desc = 'this report'
    if previous_exported_report in epoch_reports:
        ref_report = previous_exported_report
        ref_report.load_measurements()
        ref_report_desc = 'previous exported report'
    logger.info(f"using {ref_report_desc} as {epoch} reference: {ref_report.id}")

    return epoch_reports, ref_report


def write_dtt_deltal_external_calib(report):
    """export deltal_external calibration for dtt template

    """
    freqs = np.logspace(0, np.log10(7444), num=1000)
    calib = report.calcs.calcs_dtt_calibration(freqs).astype(np.complex128)
    outfile = report.gen_path("deltal_external_calib_dtt.txt")
    with open(outfile, 'w') as f:
        outstr = freqresp_to_mag_db_phase_str(freqs, calib, include_header=True)
        f.write(outstr)


def write_dtt_pcal_calib(report):
    """export pcal calibration for dtt template

    """
    freqs = np.logspace(0, np.log10(7444), num=1000)
    calib = (report.pcal.compute_pcal_correction(freqs, endstation=True)
             ).astype(np.complex128)
    outfile = report.gen_path("pcal_calib_dtt.txt")
    with open(outfile, 'w') as f:
        outstr = freqresp_to_mag_db_phase_str(freqs, calib, include_header=True)
        f.write(outstr)


def srcd2n_zpk(report, cftd=False):
    '''Returns tuple contains zeros, poles, and gain val for SRCD2N filter.

    Parameters
    ----------
    report: cmd._report.Report
        Report object from which to extract the srcd2n zpk.
    cftd: boolean, optional
        Pass through argument for inverse_sensing_srcd2n_foton_filter_zpk method
        of measurement.ProcessSensingMeasurement class. Refer to the
        documentation for that method for more details.
    '''
    _, _, _, _, chain = read_chain_from_hdf5(report.gen_path('sensing_mcmc_chain.hdf5'))
    proc_sensing_meas = report.measurements['Sensing'][0]
    z_str, p_str, _, g_str = \
        proc_sensing_meas.inverse_sensing_srcd2n_foton_filter_zpk(chain, cftd)
    sensing_sign = report.model.sensing.sensing_sign
    sign_char = '-' if str(sensing_sign).startswith('-') else ''
    zeros = tuple_from_foton_zp_format(z_str)
    poles = tuple_from_foton_zp_format(p_str)
    gain_val = float(sign_char + g_str)
    return zeros, poles, gain_val


def write_foton_tf_to_file(zpk_params, fstart, fstop, n_points, outfile,
                           rate=16384):
    """write transfer function generated by a Foton zpk design to file

    Parameters
    ----------
    zpk_params : tuple
        Tuple containing a transfer function's zeros, poles, and gain. The
        tuple is expected to be of the form ([zeros], [poles], k).
    fstart : float
        Start frequency
    fstop : float
        Stop frequency
    n_points : int
        Number of points to generate.
    outfile : str
        File path to save transfer function to.
    rate : float, optional
        Sampling rate to passed to Foton.

    Returns
    -------
    fcontent : str
        Output file content as a string.

    """
    freqs, tf = tf_from_foton_zpk(zpk_params, fstart, fstop, n_points,
                                  rate=rate)
    fcontent = ''
    for i, (freq, tf_val) in enumerate(zip(freqs, tf)):
        fcontent += f"{freq}\t{tf_val.real}\t{tf_val.imag}\n"

    with open(outfile, 'w') as f:
        f.write(fcontent)

    return fcontent


def write_epics_records_file(report):
    """export file containing epics records to be written on export

    """
    er = report.calcs.compute_epics_records(gds_pcal_endstation=False, exact=True)
    outfile = report.gen_path("export_epics_records.txt")
    np.savetxt(outfile, list(er.items()), fmt='%s')


def write_foton_designs(report):
    """Write foton filter designs to report directory for future export to front end.


    Parameters
    ----------
    report : pydarm.cmd._report.Report

    """

    model = report.model
    config = report.config
    sensing_model = model.sensing

    # sensing params
    optical_gain = sensing_model.coupled_cavity_optical_gain
    freq_cc = sensing_model.coupled_cavity_pole_frequency

    # actuation params
    act_free_params = {}

    for k in gen_config_calcs_filters_keys(config):
        stage, optic = k.split('/')
        arm_attr = f'{optic[-1].lower()}arm'
        act_model = getattr(report.model.actuation, arm_attr)

        stage_homonym = STAGE_LABEL_MAP[stage]['homonym']
        stage_unit_dpc = STAGE_LABEL_MAP[stage]['unit_drive_per_counts']
        stage_unit_nsc = STAGE_LABEL_MAP[stage]['unit_nospecial_char']

        # build structure to mimic get_act_mcmc_results() output
        act_free_params[k] = {
            'map': {
                'H_A': getattr(act_model,
                               f'{stage_homonym.lower()}_dc_gain_{stage_unit_dpc}')()
            },
            'Npct_scale': getattr(act_model,
                                  f'{stage_homonym}_{stage_unit_nsc}'.lower())
        }
        if stage == 'L2':
            act_free_params[k]['map']['H_A'] /= getattr(act_model, 'pum_coil_outf_signflip')

    # print free parameters
    logger.info(f"Hc: {optical_gain:4.4e} :: ")
    logger.info(f"1/Hc: {1/optical_gain:4.4e}")
    logger.info(f"Fcc: {freq_cc:4.4e} Hz")

    for k, v in act_free_params.items():
        stage, optic = k.split('/')
        textlabel = FREE_PARAM_LABEL_MAP[stage]['textlabel']
        map_vals = v['map']
        print(f"{textlabel}: {map_vals['H_A']:4.4e} N/A ", end='')
        print(f":: {map_vals['H_A']*v['Npct_scale']:4.4e} N/ct")

    logger.debug("filters (filter:bank | name:design string):")
    filt_export_dict = {}
    for param_name, fbanks in config['Common']['calcs_filters'].items():
        for fbank in fbanks:
            bank_name = fbank['bank_name']
            mod_name = fbank['mod_name']
            bank_slot = fbank['mod_slot']
            zeros = []
            poles = []
            if param_name == '1/Hc':
                gain_val = 1/optical_gain
            elif param_name == 'Fcc':
                gain_val = 1
                zeros = [freq_cc]
                poles = [7000]
            elif param_name == 'SRCD2N':
                zeros, poles, gain_val = srcd2n_zpk(report, cftd=True)
            elif param_name in act_free_params.keys():
                # write actuation gain in Newtons/ct
                gain_val = act_free_params[param_name]['map']['H_A'] \
                    * act_free_params[param_name]['Npct_scale']
            else:
                continue

            bank_str = f"{bank_name}:{bank_slot}"
            design_str = f"{mod_name:>10}:zpk({zeros}, {poles}, {gain_val:4.4e})"
            logger.debug(f"  {bank_str:25}  {design_str}")

            fparams = dict(filterbank=bank_name, mod_idx=bank_slot-1,
                           filter_name=mod_name, zpk_params=(str(zeros), str(poles), gain_val))
            filt_export_dict[param_name] = fparams

    with open(report.gen_path('foton_filters_to_export.json'), 'w') as fout:
        json.dump(filt_export_dict, fout)


def broadband_plot(report):
    new_report = deepcopy(report)

    freqs, processed_bb, timestamp = new_report.measurements['Broadband']
    syserr_fig = plt.figure()
    syserr_fig.suptitle(f"Pcal/DeltaL_External {timestamp}")
    ax_mag, ax_pha = syserr_fig.subplots(2, 1, sharex=True)
    ax_mag.semilogx(freqs, np.abs(processed_bb))
    ax_pha.semilogx(freqs, np.angle(processed_bb, deg=True))

    ax_mag.set_ylim(.85, 1.15)
    ax_mag.set_xlim(7, 500)
    ax_mag.grid(which='major', color='black')
    ax_mag.grid(which='minor', ls='--')
    ax_mag.set_ylabel('Magnitude')
    ax_mag.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))

    ax_pha.set_ylim(-10, 10)
    ax_pha.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax_pha.grid(which='major', color='black')
    ax_pha.grid(which='minor', ls='--')
    ax_pha.set_xlabel('Frequency [Hz]')
    ax_pha.set_ylabel('Phase [deg]')

    return [syserr_fig]


def gds_filter_generation(report):
    """generate GDS filters

    """
    report = deepcopy(report)
    filters_fname = f'gstlal_compute_strain_C00_filters_{report.IFO}.npz'
    fir_filter_gen = FIRFilterFileGeneration(report.model_file)
    fir_filter_gen.GDS(output_dir=report.path,
                       output_filename=filters_fname,
                       plots_directory=report.gen_path('fir_plots')
                       )
    figs = fir_filter_gen.figs
    return figs


def dcs_filter_generation(report):
    """generate DCS filters

    """
    report = deepcopy(report)
    filters_fname = f'gstlal_compute_strain_C00_filters_unified_{report.IFO}.npz'
    fir_filter_gen = FIRFilterFileGeneration(report.model_file)
    fir_filter_gen.DCS(output_dir=report.path,
                       output_filename=filters_fname,
                       plots_directory=report.gen_path('fir_plots_unified')
                       )
    figs = fir_filter_gen.figs
    return figs


class ReportPDF:

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.pdf = PdfPages(self.path)
        return self

    def add_figure(self, new_fig):
        if hasattr(new_fig, '__iter__'):
            for f in new_fig:
                self.pdf.savefig(f)
        else:
            self.pdf.savefig(new_fig)

    def add_figures(self, new_figs):
        for fig in new_figs:
            self.add_figure(fig)

    def __exit__(self, exception_type, exception_value, traceback):
        self.pdf.close()
        if exception_type is not None:
            os.unlink(self.path)
        return False


def add_args(parser):
    parser.add_argument(
        "time", metavar='DATETIME/REPORT_ID', nargs='?', default='now',
        help="specify date/time or report ID (default: 'now')")
    _args.add_model_option(parser)
    parser.add_argument(
        '--outdir', '-o', metavar='DIR',
        help="write report to specified directory")

    rgroup = parser.add_mutually_exclusive_group()
    rgroup.add_argument(
        '--regen', action='store_true',
        help="re-generate report with existing report model and config files")
    rgroup.add_argument(
        '--force', action='store_true',
        help="force generate report if it already exists")

    egroup = parser.add_mutually_exclusive_group()
    egroup.add_argument(
        '--epoch-sensing', dest='epoch', action='store_const',
        const=set(['sensing']),
        help="mark this report as the start of a new sensing epoch")
    egroup.add_argument(
        '--epoch-actuation', dest='epoch', action='store_const',
        const=set(['actuation']),
        help="mark this report as the start of a new actuation epoch")
    egroup.add_argument(
        '--epoch', dest='epoch', action='store_const',
        const=set(['sensing', 'actuation']),
        help=("mark this report as the start of a new epoch for "
              "both sensing and actuation"))
    parser.set_defaults(epoch=set([]))
    # we treat the hfrl epoch outside of the mutually exclusive group because
    # it need not be mutually exclusive with the sensing epoch even though it
    # is technically part of the sensing function processing.
    parser.add_argument(
        '--epoch-hfrl', dest='epoch_hfrl', action='store_true',
        help='mark this report as the start of a new HFRL epoch')

    mgroup = parser.add_mutually_exclusive_group()
    mgroup.add_argument(
        '--mcmc-only', action='store_const', dest='mcmc', const='only',
        help="run MCMC only then exit")
    mgroup.add_argument(
        '--skip-mcmc', action='store_const', dest='mcmc', const='skip',
        help="skip MCMC")

    parser.add_argument(
        '--skip-bb', action='store_true',
        help="skip broadband measurement processing")
    parser.add_argument(
        '--skip-gds', action='store_true',
        help="skip GDS FIR filter generation")

    parser.add_argument(
        '-i', '--interactive', action='store_true',
        help="interactive matplotlib plots")
    parser.add_argument(
        '--display', action=argparse.BooleanOptionalAction, default=True,
        help="display report after generation or not")


def main(args):
    """generate/view full calibration report

    Calibration reports are based on measurement sets, which are
    complete sets of all the sensing, actuation, and PCal response
    function measurements needed to model the calibration function.
    The measurements themselves are executed with the `measure`
    sub-command.

    A measurement set for a given time consists of the most recent
    sensing/actuaion/PCal measurements before that time.  Each
    measurement set is identified by the date-time of its latest
    measurement.  For any measurement set there can be a report whose
    ID is the timestamp of the corresponding measurement set.  The
    command is able to gather measurement sets from the available
    sensing/actuation/pcal measurements, and generate reports based on
    them.

    Calibration reports consist of the following for each measurement
    type: MCMC summary (including a corner plot), a "history" plot,
    and a GPR result. In addition, fresh FIR filters are generated along
    with the generation of each new report based on the pyDARM parameter
    model set once it's been populated with the free parameters as estimated
    by the MCMC process.

    A report tagging system is used to indicate the set of reports to consider
    in the "history" plots and the GPR processing, as well as to identify
    which report's model should be considered the set's "reference".

    We define an `epoch` to be the first report in a given set (i.e. the
    report that marks the starting boundary of a set). The end of each set
    is marked by the start of the next epoch or, if there is none, the most
    recent report. The `epoch` tag is interpreted as representing the start of
    an epoch for the sensing and acutation functions simultaneously. Similarly,
    the `epoch-sensing` and `epoch-actuation` tags do the same for only their
    corresponding measurements.

    The `valid` tag identifies reports that should be included in the GPR
    processing and the "history" comparison plots.

    The `exported` tag is created when a report has been exported to the
    front end at either L1 or H1. The most recent exported report should
    be considered the reference (i.e. containing the reference model) in
    the MCMC residuals, GPR, and history residuals.

    If no arguments are provided, this command will generate or view
    the report corresponding to the latest measurement set.  If a time
    argument is provided, the latest measurement set for that time
    will be processed.  If a report ID is provided, the report
    corresponding to that ID will be produced.
    """
    logger.info(f"pydarm version {__version__}")

    if args.mcmc == 'skip' and not args.regen:
        raise CMDError("--skip-mcmc option only valid with --regen.")

    if args.regen and args.model != DEFAULT_MODEL_PATH:
        raise CMDError("can not specify alternate model file with --regen, use --force instead.")

    try:
        report = Report.find(args.time)
        mset = report.mset
        logger.info(f"existing report found: {report.path}")
        logger.info("using report's measurement set...")
    except FileNotFoundError:
        logger.info("searching measurement sets...")
        mset = MeasurementSet.find(args.time, config_file=args.config,
                                   skip_bb=args.skip_bb)
        logger.info(f"measurement set found: {mset.id}")
        try:
            report = Report.find(mset.id)
            logger.info(f"corresponding report found: {report.path}")
        except FileNotFoundError:
            report = None

    if args.outdir:
        report_dir = args.outdir
        try:
            report = Report(report_dir)
            logger.info(f"report found at alternate report path: {report_dir}")
        except FileNotFoundError:
            report = None
            logger.info(f"using alternate report path: {report_dir}")
    elif report:
        report_dir = report.path
    else:
        report_dir = Report.default_path(mset.id)

    config_file = args.config
    model_file = args.model
    if report:
        if args.force:
            logger.info("force re-creation of existing report...")
            report = None
        elif args.regen:
            logger.info("regenerating existing report (using report model and config files)...")
            config_file = report.config_file
            model_file = report.model_file
            report = None
    else:
        logger.info(f"generating report {report_dir}...")

    # set plotting interactive mode
    plt.interactive(args.interactive)

    ##########

    # set CAL_DATA_ROOT env var for core
    CAL_DATA_ROOT = set_cal_data_root()

    if report is None:
        # create report
        report = Report.create(
            mset,
            config_file,
            model_file,
            path=report_dir,
        )
        log_to_file(logger, report.gen_path("log"))

        logger.info(f"model file: {model_file}")
        logger.info(f"config file: {config_file}")

        write_pydarm_version(report.gen_path('pydarm_version'))
        report.load_measurements()

        output_figs = []

        ##########
        # MCMC generation

        if args.mcmc != 'skip':
            logger.info("running sensing MCMC...")
            sensing_MCMC(report)

            logger.info("running actuation MCMC...")
            actuation_MCMC(report)

            # FIXME: log params

            # update model ini with new fit params
            model_config = report.model._config
            params = report.gen_free_params_ini_dict()
            logger.info("writing fit parameters to model file "
                        f"{report.model_file}...")
            base, ext = os.path.splitext(report.model_file)
            orig_out = base + '.orig' + ext
            orig_parsed_out = base + '.orig-parsed' + ext
            os.rename(report.model_file, orig_out)
            with open(orig_parsed_out, 'w') as f:
                model_config.write(f)
            model_config.read_dict(params)
            with open(report.model_file, 'w') as f:
                model_config.write(f)

            if args.mcmc == 'only':
                return

        ##########
        # find last exported

        try:
            previous_exported_report = list_reports(
                exported_only=True,
                before=report.id_gpstime(),
            )[0]
            logger.info(f"previous exported report: {previous_exported_report.id}")
        except IndexError:
            previous_exported_report = None
            logger.info("no previously exported report found")

        ##########
        # sensing GPR and history

        # find all sensing epoch reports
        if 'sensing' in args.epoch:
            logger.info("new epoch, ignoring past reports for sensing.")
            report.add_tags('epoch-sensing')
            sensing_epoch_reports = []
            sensing_ref_report = report
        else:
            sensing_epoch_reports, sensing_ref_report = \
                find_epoch_reports('sensing', report, previous_exported_report)

        # find sensing hfrl epoch report
        sensing_hfrl_epoch_reports, _ = \
            find_epoch_reports('hfrl', report, previous_exported_report)
        if args.epoch_hfrl or sensing_hfrl_epoch_reports == []:
            logger.info("marking new report as an HFRL epoch")
            logger.info("ignoring past HFRL measurements (if any).")
            if args.epoch_hfrl:
                report.add_tags('epoch-hfrl')
            sensing_hfrl_epoch_boundary_report = report
        else:
            sensing_hfrl_epoch_boundary_report = sensing_hfrl_epoch_reports[-1]

        logger.info("generating sensing history...")
        fig_sens_hist = sensing_history(report, sensing_epoch_reports[:9], sensing_ref_report)
        output_figs.append(fig_sens_hist)

        logger.info("generating sensing GPR...")
        fig_sens_gpr = sensing_GPR(report, sensing_epoch_reports, sensing_ref_report,
                                   sensing_hfrl_epoch_boundary_report)
        output_figs.append(fig_sens_gpr)

        ##########
        # actuation GPR and history

        # find past reports in actuation epoch
        if 'actuation' in args.epoch:
            logger.info("new epoch, ignoring past reports for actuation.")
            report.add_tags('epoch-actuation')
            actuation_epoch_reports = []
            actuation_ref_report = report
        else:
            actuation_epoch_reports, actuation_ref_report = \
                find_epoch_reports('actuation', report, previous_exported_report)

        logger.info("generating actuation history...")
        fig_act_hist = actuation_history(report, actuation_epoch_reports[:9], actuation_ref_report)
        output_figs.append(fig_act_hist)

        logger.info("generating actuation GPR...")
        fig_act_gpr = actuation_GPR(report, actuation_epoch_reports, actuation_ref_report)
        output_figs.append(fig_act_gpr)

        logger.info("generating Pcal to GDS and prepending figure...")
        fig_pcalGDS = pcal_to_gds(report)
        output_figs.insert(0, fig_pcalGDS)

        ##########
        # CALCS outputs

        zpk_params = srcd2n_zpk(report)
        logger.info(f"Inverse sensing z: {zpk_params[0]}")
        logger.info(f"Inverse sensing p: {zpk_params[1]}")
        logger.info(f"Inverse sensing k: {zpk_params[2]}")

        #####
        # FIXME: the CALCSModel expects this inverse sensing TF file
        # to be specified in the ini, needed for the EPICS and dtt
        # calib calc methods below.  so we write out the file to the
        # report dir and then update the ini to point to that location
        # at an absolute path, so it doesn't try to resolve against
        # CAL_DATA_ROOT.  but that means we have an abs path in the
        # ini, which will break as the ini moves around.  we need a
        # better way to pass this location to CALCSModel, so that we
        # don't have to do these hacky shenanigans.

        # generate inverse sensing foton tf and place it in the cal svn
        tf_dir = os.path.join(CAL_DATA_ROOT, 'Runs/O4', IFO, 'Measurements/Foton')
        tf_fname = f"{IFO}CALCS_InverseSensingFunction_Foton_tf.txt"
        inv_sensing_tf_file = os.path.abspath(report.gen_path(tf_fname))

        os.makedirs(tf_dir, exist_ok=True)
        write_foton_tf_to_file(zpk_params, 0.01, 10000, 1001,
                               inv_sensing_tf_file)

        model_config = report.model._config
        model_config.read_dict({'calcs': {'foton_invsensing_tf':
                                          inv_sensing_tf_file}})
        with open(report.model_file, 'w') as f:
            model_config.write(f)

        # FIXME
        #####

        write_dtt_deltal_external_calib(report)
        write_epics_records_file(report)
        write_foton_designs(report)

        ##########
        # PCAL outputs

        write_dtt_pcal_calib(report)

        ##########
        # GDS FIR filter generation

        if not args.skip_gds:
            logger.info("generating GDS filters...")
            fig_gds_filt = gds_filter_generation(report)
            output_figs.append(fig_gds_filt)

            logger.info("generating DCS filters...")
            fig_dcs_filt = dcs_filter_generation(report)
            output_figs.append(fig_dcs_filt)

        ##########
        # write report PDF

        with ReportPDF(report.report_file) as rpdf:
            rpdf.add_figures(output_figs)

        logger.info("report generation complete.")
        logger.info(f"report file: {report.report_file}")
        if args.interactive:
            input('press enter to exit')

    if args.display:
        if not os.path.exists(report.report_file):
            raise CMDError(f"report file not found! ({report.report_file})")
        logger.info(f"displaying report {report.report_file}...")
        subprocess.run(['xdg-open', report.report_file], check=True)
