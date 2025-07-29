import numpy as np
import dttxml
import h5py
from glob import glob
from gwpy.timeseries import TimeSeriesDict as tsd
from joblib import Memory
import os

from ._args import freq_from_spec
from ._const import CAL_CONFIG_ROOT
from .uncertainty import (
    TDCF_SPAN,
    DEFAULT_TRIALS,
    DEFAULT_FREQ_ARRAY
)

from ..plot import BodePlot
from ..uncertainty import DARMUncertainty


@Memory('_cache').cache
def bbGDSPcal(report, filepath):
    """prepare the data for the broadband to GDS plot
    this is GDS/Pcal

    """
    bb = dttxml.DiagAccess(filepath)
    pcalarm = 'X' if report.IFO == 'L1' else 'Y'
    meas = bb.xfer(f'{report.IFO}:CAL-DELTAL_EXTERNAL_DQ',
                   f'{report.IFO}:CAL-PCAL{pcalarm}_RX_PD_OUT_DQ')
    startGPS = int(meas.gps_second)
    avs = int(meas.averages)
    fft = int(round(1/(meas.FHz[1]-meas.FHz[0])))
    overlap = 0.5  # have to hardcode, cant find in dttxml parameters

    duration = int(round(fft + fft*(1-overlap)*(avs-1)))

    data = tsd.get([f'{report.IFO}:GDS-CALIB_STRAIN',
                   f'{report.IFO}:CAL-PCAL{pcalarm}_RX_PD_OUT_DQ'],
                   startGPS, startGPS+duration)

    tf_data = data[f'{report.IFO}:CAL-PCAL{pcalarm}_RX_PD_OUT_DQ'].transfer_function(
        data[f'{report.IFO}:GDS-CALIB_STRAIN'],
        fftlength=fft, overlap=overlap, window='hann')
    coh_data = data[f'{report.IFO}:CAL-PCAL{pcalarm}_RX_PD_OUT_DQ'].coherence(
        data[f'{report.IFO}:GDS-CALIB_STRAIN'],
        fftlength=fft, overlap=overlap, window='hann')

    freq = np.array(tf_data.frequencies.value, dtype=np.float64)
    tf = np.array(tf_data.value, dtype=np.complex128)
    coh = np.array(coh_data.value, dtype=np.float64)
    freq = freq[(coh > 0.99)]
    tf = tf[(coh > 0.99)]
    coh = coh[(coh > 0.99)]
    unc = np.sqrt((1.0-coh)/(2.0*(coh+1e-6)*avs))

    tf_cor = report.pcal.compute_pcal_correction(freq, endstation=True, arm=pcalarm)
    tf /= tf_cor
    tf *= report.model.sensing.mean_arm_length()
    return freq, tf, coh, unc


@Memory('_cache').cache
def ssGDSPcal(report, filepath):
    """prepare the data for the swept sines to GDS plot
    this is GDS/Pcal

    """
    if filepath.endswith('.hdf5'):
        ss = h5py.File(filepath, 'r')
        try:
            chanA = f'{report.IFO}:CAL-PCALY_RX_PD_OUT'
            chanB = f'{report.IFO}:LSC-DARM_IN1'
            freq = ss[chanB][chanA]['Frequencies'][()].astype(np.float64)
        except KeyError:
            chanA = f'{report.IFO}:CAL-PCALY_RX_PD_OUT_DQ'
            chanB = f'{report.IFO}:LSC-DARM_IN1_DQ'
            freq = ss[chanB][chanA]['Frequencies'][()].astype(np.float64)
        startTimes = ss[chanB][chanA]['StartTimes'][()].astype(int)
        endTimes = ss[chanB][chanA]['EndTimes'][()].astype(int)
        minDriveTime = ss['parameters']['minDriveTime'][()].astype(int)
        driveCycles = ss['parameters']['drivingCycles'][()].astype(int)
        avs = ss['parameters']['averages'][()].astype(int)
    elif filepath.endswith('.xml'):
        # Dtt templates do not save the start gps times for each point,
        # only saving whole sweep start time.
        return [], [], [], []
    else:
        return [], [], [], []

    data = tsd.get([f'{report.IFO}:GDS-CALIB_STRAIN', f'{report.IFO}:CAL-PCALY_RX_PD_OUT_DQ'],
                   min(startTimes), max(endTimes))
    sampleRate = int(data[f'{report.IFO}:GDS-CALIB_STRAIN'].sample_rate.value)
    initialTime = int(data[f'{report.IFO}:GDS-CALIB_STRAIN'].t0.value)
    tf = np.zeros(len(freq), dtype=np.complex128)
    coh = np.zeros(len(freq), dtype=np.float64)
    for i in range(len(freq)):
        fft = max(minDriveTime, (driveCycles / freq[i]))
        sampInMeas = int(round(fft * sampleRate, 0))

        t0 = (startTimes[i] - initialTime) * sampleRate
        A = np.float64(data[f'{report.IFO}:CAL-PCALY_RX_PD_OUT_DQ'][t0: t0 + avs*sampInMeas])
        B = np.float64(data[f'{report.IFO}:GDS-CALIB_STRAIN'][t0: t0 + avs*sampInMeas])
        A.sample_rate = 1
        B.sample_rate = 1

        tfArray = A.transfer_function(B, fftlength=sampInMeas, overlap=0, window='hann')
        cohArray = A.coherence(B, fftlength=sampInMeas, overlap=0, window='hann')
        index = int(round(((freq[i]/sampleRate) - tfArray.f0.value) / tfArray.df.value))

        tf[i] = np.complex128(tfArray[index])
        coh[i] = np.float64(cohArray[index])
    tf = tf[(freq > 10)]
    coh = coh[(freq > 10)]
    freq = freq[(freq > 10)]
    unc = np.sqrt((1.0-coh)/(2.0*(coh+1e-6)*avs))

    tf_cor = report.pcal.compute_pcal_correction(freq, endstation=True, arm='Y')
    tf /= tf_cor
    tf *= report.model.sensing.mean_arm_length()
    return freq, tf, coh, unc


def undertaintyData(report):
    """prepare an uncertainty plot valid shortly before the calibration sweeps
    this is Pcal/GDS

    """
    # Because of needing gpr and mcmc, this whole method needs to be run last.
    unc_config = f'{CAL_CONFIG_ROOT}/pydarm_uncertainty_{report.IFO}.ini'
    sensing_mcmc_file = report.gen_path('sensing_mcmc_chain.hdf5')
    sensing_gpr_file = report.gen_path('sensing_gpr.hdf5')
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
    actuation_mcmc_files_dict = {'xarm': {}, 'yarm': {}}
    actuation_gpr_files_dict = {'xarm': {}, 'yarm': {}}
    for arm, stages in actuation_file_map.items():
        for stage, base in stages.items():
            mcmc_file = report.gen_path(f'{base}_mcmc_chain.hdf5')
            gpr_file = report.gen_path(f'{base}_gpr.hdf5')
            if os.path.exists(mcmc_file):
                actuation_mcmc_files_dict[arm][stage] = mcmc_file
            if os.path.exists(gpr_file):
                actuation_gpr_files_dict[arm][stage] = gpr_file

    darm_unc = DARMUncertainty(
        report.model_file,
        uncertainty_config=unc_config,
        sensing_mcmc_file=sensing_mcmc_file,
        sensing_gpr_file=sensing_gpr_file,
        actuation_mcmc_files_dict=actuation_mcmc_files_dict,
        actuation_gpr_files_dict=actuation_gpr_files_dict
    )
    channels = darm_unc.tdcf_channel_list()
    gps = report.id_int() - 600  # choose a time 10 minutes before SS sweeps
    tdcf_gps_start = gps - TDCF_SPAN
    tdcf_gps_end = gps + TDCF_SPAN
    data = tsd.get(
        channels,
        tdcf_gps_start, tdcf_gps_end
    )
    samples = darm_unc.compute_response_uncertainty(
        gps,
        freq_from_spec(DEFAULT_FREQ_ARRAY),
        trials=DEFAULT_TRIALS,
        data=data
    )
    response_mag_quant, response_pha_quant = darm_unc.response_quantiles(samples)
    return freq_from_spec(DEFAULT_FREQ_ARRAY), response_mag_quant, response_pha_quant


def pcal_to_gds(report):
    """generate plot of pcal swept sine and broad band overlaid to the uncertainty

    """

    freqBB, tfBB, cohBB, uncBB = bbGDSPcal(
        report,
        glob(f'{report.gen_mpath()}/PCAL*2DARM_BB*')[0])
    freqSS, tfSS, cohSS, uncSS = ssGDSPcal(
        report,
        glob(f'{report.gen_mpath()}/PCAL*2DARM_SS*')[0])
    freqUnc, magUncSet, phaUncSet = undertaintyData(report)

    title = f"{report.IFO} PCal over GDS \n"
    subtitleText = f"Pcal Correction drawn from {report.model_file}"
    ifo_color = 'r' if report.IFO == 'H1' else 'b'

    # transfer function plot
    pcal_gds_fig = BodePlot(title=title)
    pcal_gds_fig.ax_mag.set_title(subtitleText, fontsize=8)

    pcal_gds_fig.error(
        freqBB,
        1/tfBB,  # Take inverse because uncertainty is Pcal/GDS, and people are familiar with it
        uncBB,
        fmt='.',
        label='BroadBand Injection (PCal X)',
        markersize=6,
        elinewidth=0.5,
        color='indigo',
        ecolor='indigo',
        zorder=1)
    pcal_gds_fig.error(
        freqSS,
        1/tfSS,  # Take inverse because uncertainty is Pcal/GDS, and people are familiar with it
        uncSS,
        fmt='.',
        label='SweptSine Injection (PCal Y)',
        markersize=12,
        elinewidth=1,
        color='green',
        ecolor='green',
        zorder=2)
    pcal_gds_fig.ax_mag.plot(freqUnc, magUncSet[1, :], color=ifo_color,
                             label=r'Median Uncertainty', alpha=0.4, zorder=3)
    pcal_gds_fig.ax_mag.plot(freqUnc, magUncSet[0, :], linestyle='--', color=ifo_color,
                             label=r'$1 \sigma$ Uncertainty', alpha=0.4, zorder=3)
    pcal_gds_fig.ax_mag.plot(freqUnc, magUncSet[2, :], linestyle='--', color=ifo_color,
                             alpha=0.4, zorder=3)
    pcal_gds_fig.ax_mag.fill_between(freqUnc, magUncSet[0, :],
                                     magUncSet[2, :], color=ifo_color, alpha=0.1, zorder=3)
    pcal_gds_fig.ax_phase.plot(freqUnc, 180/np.pi*phaUncSet[1, :],
                               color=ifo_color, alpha=0.4, zorder=3)
    pcal_gds_fig.ax_phase.plot(freqUnc, 180/np.pi*phaUncSet[0, :], linestyle='--',
                               color=ifo_color, alpha=0.4, zorder=3)
    pcal_gds_fig.ax_phase.plot(freqUnc, 180/np.pi*phaUncSet[2, :], linestyle='--',
                               color=ifo_color, alpha=0.4, zorder=3)
    pcal_gds_fig.ax_phase.fill_between(freqUnc, 180/np.pi*phaUncSet[0, :],
                                       180/np.pi*phaUncSet[2, :], color=ifo_color,
                                       alpha=0.1, zorder=3)

    pcal_gds_fig.ax_mag.set_yscale('linear')
    pcal_gds_fig.ax_mag.set_yscale('linear')
    pcal_gds_fig.ax_mag.set_ylim(0.92, 1.08)
    pcal_gds_fig.ax_mag.set_yticks(np.arange(0.92, 1.08, 0.01))
    pcal_gds_fig.ax_mag.set_yticklabels(
        np.round(np.arange(0.92, 1.08, 0.01), decimals=2),
        fontsize=11)
    pcal_gds_fig.ax_phase.set_ylim(-8, 8)
    pcal_gds_fig.ax_phase.set_yticks(np.arange(-8, 9, 1))
    pcal_gds_fig.ax_phase.set_yticklabels(np.arange(-8, 9, 1), fontsize=11)
    pcal_gds_fig.ax_mag.set_xlim(10, 1400)
    pcal_gds_fig.ax_phase.set_xlim(10, 1400)
    pcal_gds_fig.ax_mag.set_ylabel('PCal / GDS Disp. [Magnitude (m/m)]')
    pcal_gds_fig.ax_phase.set_ylabel('PCal / GDS Disp. [Phase (deg)]')
    pcal_gds_fig.ax_mag.legend(ncol=2)

    # Wrap up and save figure
    pcal_gds_fig.save(
        report.gen_path(
            "pcal_to_GDS.png"
        )
    )
    return pcal_gds_fig.fig
