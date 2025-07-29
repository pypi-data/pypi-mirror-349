import os
from glob import glob
from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker

from ..measurement import RoamingLineMeasurementFile

from ._log import logger
from ._const import CAL_CONFIG_ROOT


def sensing_GPR(new_report, epoch_reports, ref_report, hfrl_epoch_report):
    """calculate sensing GPR

    Takes as input the current report, the list of all reports from
    the current sensing epoch, and the reference report.

    """
    all_reports = [new_report] + epoch_reports
    hfrl_epoch_boundary = hfrl_epoch_report.id_gpstime()

    # try to get the gpr frequency range & plot range from
    # config file (cmd yaml). otherwise use the same defaults
    # we've used before.
    sensing_cfg = new_report.config['Sensing']['params']
    try:
        sensing_gpr_frange = [sensing_cfg['gpr_fmin'],
                              sensing_cfg['gpr_fmax']]
    except Exception:
        sensing_gpr_frange = [5, 4100]
        logger.warning("WARNING: Unable to read parameter from config. "
                       f"Defaulting to gpr_freq_range={sensing_gpr_frange}")
    try:
        frange_plot = sensing_cfg['gpr_freq_range_plot']
    except Exception:
        frange_plot = [4, 4500]
        logger.warning("WARNING: Unable to read parameter from config. "
                       f"Defaulting to frange_plot={frange_plot}")
    try:
        rbf_length_scale = sensing_cfg['rbf_length_scale']
    except Exception:
        rbf_length_scale = 1.0
        logger.warning("WARNING: Unable to read parameter from config. "
                       f"Defaulting to rbf_length_scale={rbf_length_scale}")
    try:
        rbf_length_scale_limits = sensing_cfg['rbf_length_scale_limit']
    except Exception:
        rbf_length_scale_limits = [0.5, 1]
        logger.warning("WARNING: Unable to read parameter from config. "
                       f"Defaulting to rbf_length_scale_limits={rbf_length_scale_limits}")

    # FIXME: take this from input args with default option
    frequencies = np.logspace(np.log10(1), np.log10(5000), 100)

    measurement_list = []
    timestamp_list = []
    fmin_list = []
    fmax_list = []
    ref_fmin = None
    ref_fmax = None
    ref_measurement = None
    for ireport in deepcopy(all_reports):
        processed_sensing, timestamp = ireport.measurements['Sensing']
        mcmc_data = ireport.get_sens_mcmc_results()

        # skip duplicate measurements
        if timestamp in timestamp_list:
            continue

        timestamp_list.append(timestamp)
        measurement_list.append(processed_sensing)
        fmin_list.append(mcmc_data['fmin'])
        fmax_list.append(mcmc_data['fmax'])

        if ireport.id == ref_report.id:
            ref_measurement = processed_sensing
            ref_fmin = mcmc_data['fmin']
            ref_fmax = mcmc_data['fmax']

    # Now we will read the HF roaming line results and process them to be
    # included in the GPR
    hf_meas_filenames = glob(new_report.gen_mpath('hf_roaming_lines', 'DARM*.txt'))
    hf_pcal_unc_corr = os.path.join(CAL_CONFIG_ROOT,
                                    "pcal_high_frequency_uncertainty_O4a",
                                    "etm_deformation_uncertainty.txt")
    # FIXME: this handling of the HF measurement files is terrible.
    if hf_meas_filenames == []:
        logger.warning("WARNING: No HFRL files found at "
                       f"{new_report.gen_mpath('hf_roaming_lines')}")
    else:
        logger.info(f"Found HF tf files: {hf_meas_filenames}")
    hf_meas_files = [RoamingLineMeasurementFile(f, hf_pcal_unc_corr)
                     for f in hf_meas_filenames]

    # filter measurements by date; include only those valid during the
    # valid epoch, if any.
    # also ignore individual measurements where the coherence is nan
    #
    # for determining which HF measurements to process use the
    # true epoch report as the starting bound
    epoch_start_report = all_reports[-1]
    epoch_end_report = new_report
    logger.info(f"HF epoch: {epoch_start_report.id} -- {epoch_end_report.id}")
    hf_measurements = []
    for hfm in hf_meas_files:
        mlist = []
        for m in hfm.measurements:
            if np.isnan(m.coh):
                logger.debug(f"Discarding NAN coherence HF measurements: {m}")
                continue
            mag_exp_scale = np.log10(np.abs(m.get_raw_tf()[1][0]))
            if mag_exp_scale > 10.:
                logger.debug("Discarding possible glitch measurement "
                             f": {m}")
                continue
            # FIXME: indefensible hack to get rid of buggy calc with supposedly
            # high coherence.
            # need to fix the HFRL measurement code. -LD
            # if m.navg > 10:
            #     logger.debug(f"Discarding navg>10 measurement to kill crazy TF: {m}")
            #     continue

            if m.coh >= 0.99999:
                logger.debug(f"Discarding coh=1 measurement: {m}")
                continue

            mlist.append(m)

        # filter out any measurements in a different epoch
        for m in mlist:
            m_start, m_end = m.gps_segment

            # As per Cal meeting on 01/31/2024: we will allow the processing of
            # HFRL measurements from previous epochs if we don't anticipate any
            # significant changes. So I comment out the following three
            # lines. -LD

            # if not m_start >= epoch_start.gps():
            #     # print("Discarding measurement before "
            #     #       f"epoch start ({m_start}): {m}")
            #     continue

            # Don't use HFRL measurements that include data from after
            # the epoch ends. I.E. don't use measurements from the future.
            if not m_end <= epoch_end_report.gps():
                continue

            if not m_start >= hfrl_epoch_boundary.gps():
                continue
            logger.info(f"Including HFRL measurement: {m}")
            hf_measurements.append(m)

    logger.info("Including high frequency measurements from")
    logger.info(f"{hfrl_epoch_boundary.gps()} to {epoch_end_report.gps()}")

    # write log of high freq roaming line calcs included
    with open(new_report.gen_path("hf_roaming_lines.txt"), 'w') as f:
        fhdr = ("# Frequency (Hz), tf mag, tf phase (rad), coherence, "
                "# of averages, "
                "Kappa_C, Fcc, gps start, gps end, datetime start, "
                "datetime end")
        f.write(fhdr + '\n')
        for hfm in hf_measurements:
            f.write(str(hfm) + "\n")

    hf_freqs = [x.freq for x in hf_measurements]

    hf_meas_x = list(map(lambda x: (ref_report.model_file, x),
                         hf_measurements))

    # run GPR
    frequencies = np.sort(list(frequencies) + hf_freqs)
    median, unc, cov, rsdls, tdcfs, gpr_ = ref_measurement.run_gpr(
        frequencies, measurement_list,
        ref_fmin, ref_fmax,
        fmin_list=fmin_list, fmax_list=fmax_list,
        gpr_flim=(sensing_gpr_frange[0], sensing_gpr_frange[1]),
        save_to_file=new_report.gen_path('sensing_gpr.hdf5'),
        roaming_measurement_list_x=hf_meas_x,
        RBF_length_scale=rbf_length_scale,
        RBF_length_scale_limits=rbf_length_scale_limits
    )

    #  ============================ Plots ===============================
    mag = np.abs(median)
    phase = np.angle(median) * 180.0 / np.pi

    stacked_meas, tdcfs = ref_measurement.stack_measurements(
        measurement_list,
        ref_fmin, ref_fmax, fmin_list, fmax_list,
        roaming_measurement_list_x=hf_meas_x
    )

    sensing_gpr_figs = []
    fig, axes = plt.subplots(nrows=2, ncols=1)
    sensing_gpr_figs.append(fig)
    fig.suptitle("Sensing GPR")
    ax0, ax1 = axes.flat

    ax0.plot(frequencies, mag, 'b-', label='Median')
    ax0.fill_between(frequencies, mag - unc, mag + unc, alpha=0.5,
                     fc='b', label='68% C.I.')
    ax0.set_xlim(frange_plot)
    ax0.set_ylim([0.80, 1.2])
    ax0.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
    ax0.set_ylabel(r'Mag (meas/model)')

    ax1.plot(frequencies, phase, 'b-', label='Median')
    ax1.fill_between(
        frequencies, phase - unc*180.0/np.pi, phase + unc*180.0/np.pi,
        alpha=0.5, fc='b', label='68% C.I.',
    )

    plot_handles = []
    plot_labels = []
    for i, meas in enumerate(stacked_meas):
        errbar_handle = ax0.errorbar(
            meas[0], np.abs(meas[4]),
            marker='o', markersize=10, linestyle='',
            yerr=meas[3],
        )

        # only add the following handles and labels for measurements
        # included as part of a sweep, not the high freq roaming line
        # measurements
        if i < len(timestamp_list):
            plot_handles.append(errbar_handle)
            plot_labels.append(f"meas. {timestamp_list[i]} of "
                               f"report {all_reports[i].id}")

        ax1.errorbar(
            meas[0],
            np.angle(meas[4])*180.0/np.pi,
            marker='o', markersize=10,
            linestyle='', yerr=meas[3]*180.0/np.pi,
        )

    ax1.set_xlim(frange_plot)
    ax1.set_ylim([-15, 15])
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(2))
    ax1.set_xlabel(r'Frequency (Hz)')
    ax1.set_ylabel(r'Phase (meas/model) [deg]')

    for ax in axes.flat:
        ax.grid(which='major', color='black')
        ax.grid(which='minor', ls='--')
        ax.set_xscale('log')
        ax.legend(loc='lower center', ncol=2, handlelength=2)
        ax.axvline(sensing_gpr_frange[0], ls='--', color='C06')
        ax.axvline(sensing_gpr_frange[1], ls='--', color='C06')

    fig.tight_layout(rect=(0, 0, 1, .87))
    # ax0.legend(
    fig.legend(
        handles=plot_handles,
        labels=plot_labels,
        bbox_to_anchor=(.05, .83, .92, .1),
        ncol=3,
        mode='expand',
        fontsize='small',
        numpoints=1,
        markerscale=1,
        bbox_transform=fig.transFigure,
        loc='lower left',
    )

    plt.savefig(new_report.gen_path('sensing_gpr.png'), bbox_inches='tight',
                pad_inches=0.2)
    return sensing_gpr_figs


def actuation_GPR(new_report, epoch_reports, ref_report):
    """Calculate actuation GPR

    Takes as input the current report, the list of all reports from
    the current actuation epoch, and the reference report.

    """
    all_reports = deepcopy([new_report] + epoch_reports)

    base_config = ref_report.config['Actuation']

    actuation_gpr_figs = []
    frequencies = np.logspace(np.log10(1), np.log10(5000), 100)

    # FIXME: take values from config['Actuation'][<stage>] section
    UIM_gpr_frange = [10, 50]
    PUM_gpr_frange = [10, 500]
    TST_gpr_frange = [10, 800]

    stage_frange_dict = {
        'L1': UIM_gpr_frange,
        'L2': PUM_gpr_frange,
        'L3': TST_gpr_frange,
    }

    # keep a list of actuation measurements and their mcmc fit ranges by
    # stage and by optic.
    act_meas_dict = {
        'L1': {'EX': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []},
               'EY': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []}},
        'L2': {'EX': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []},
               'EY': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []}},
        'L3': {'EX': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []},
               'EY': {'fmin': [], 'fmax': [],
                      'measurements': [], 'timestamps': []}},
    }

    for mi, ireport in enumerate(all_reports):

        for stage, optics in base_config.items():
            if stage == 'params':
                continue

            for optic, config in optics.items():
                if optic == 'params':
                    continue

                name = f'Actuation/{stage}/{optic}'

                # here we grab the corresponding measurement from the
                # reference report.
                ref_processed_meas, ref_timestamp = \
                    ref_report.measurements[name]

                # we use act_val to avoid having to write the dictionary
                # indexing every time it needs to be accessed
                act_val = act_meas_dict[stage][optic]

                # we add the reference measurement if it isn't already in the
                # list. The reference should be first to be added to the list.
                if ref_processed_meas not in act_val['measurements']:
                    act_val['measurements'].append(ref_processed_meas)
                    act_val['timestamps'].append(ref_timestamp)
                    ref_mcmc_data = ref_report.get_act_mcmc_results()
                    ref_act_unit_mcmc_params = ref_mcmc_data['/'.join([stage,
                                                                       optic])]
                    act_val['fmin'].append(ref_act_unit_mcmc_params['fmin'])
                    act_val['fmax'].append(ref_act_unit_mcmc_params['fmax'])

                # now we take the corresponding measurement from the
                # report we're iterating over
                processed_actuation, timestamp = ireport.measurements[name]
                # skip duplicate measurements
                # Now we determine whether to add the "current" report's
                # measurement to the list.
                if timestamp in act_val['timestamps']:
                    continue

                mcmc_data = ireport.get_act_mcmc_results()
                act_unit_mcmc_params = mcmc_data['/'.join([stage, optic])]

                act_val['timestamps'].append(timestamp)
                act_val['measurements'].append(processed_actuation)
                act_val['fmin'].append(act_unit_mcmc_params['fmin'])
                act_val['fmax'].append(act_unit_mcmc_params['fmax'])

    # run GPR for all measurements
    for stage, optics in base_config.items():
        if stage == 'params':
            continue
        for optic, config in optics.items():
            if optic == 'params':
                continue

            meas_list = act_meas_dict[stage][optic]['measurements']
            fmin_list = act_meas_dict[stage][optic]['fmin']
            fmax_list = act_meas_dict[stage][optic]['fmax']
            ref_meas = ref_report.measurements[f'Actuation/{stage}/{optic}'][0]
            ref_meas_idx = meas_list.index(ref_meas)

            gpr_fname = f'actuation_{stage}_{optic}_gpr.hdf5'
            median, unc, cov, residuals, tdcfs = ref_meas.run_gpr(
                frequencies, deepcopy(meas_list),
                fmin_list[ref_meas_idx], fmax_list[ref_meas_idx],
                fmin_list=fmin_list, fmax_list=fmax_list,
                gpr_flim=(stage_frange_dict[stage][0],
                          stage_frange_dict[stage][1]),
                save_to_file=new_report.gen_path(gpr_fname),
            )

            #  ============================ Plots =============================
            frange_plot = [5, 2000]  # FIXME: make tunable via cmd config
            mag = np.abs(median)
            phase = np.angle(median)*180.0 / np.pi

            stacked_meas, tdcfs = ref_meas.stack_measurements(
                meas_list,
                fmin_list[ref_meas_idx],
                fmax_list[ref_meas_idx],
                fmin_list,
                fmax_list,
            )

            name = f'Actuation/{stage}/{optic}'
            fig, axes = plt.subplots(nrows=2, ncols=1)
            fig.suptitle(f"{name} GPR")
            ax0, ax1 = axes.flat

            ax0.plot(frequencies, mag, 'b-', label='Median')
            ax0.fill_between(frequencies, mag - unc, mag + unc,
                             alpha=0.5, fc='b', label='68% C.I.')

            plot_handles = []
            plot_labels = []
            for i, meas in enumerate(stacked_meas):
                errbar_handle = ax0.errorbar(
                    meas[0],
                    np.abs(meas[4]),
                    marker='o',
                    markersize=10, linestyle='',
                    yerr=meas[3],
                )
                plot_handles.append(errbar_handle)
                plot_labels.append(f"{all_reports[i].id}")

                ax1.errorbar(meas[0],
                             np.angle(meas[4])*180.0/np.pi,
                             marker='o', markersize=10, linestyle='',
                             yerr=meas[3]*180.0/np.pi)

            ax0.set_xlim(frange_plot)
            ax0.set_ylim([0.9, 1.1])
            ax0.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
            ax0.set_ylabel(r'Mag (meas/model)')

            ax1.plot(frequencies, phase, 'b-', label='Median')
            ax1.fill_between(frequencies, phase - unc*180.0/np.pi,
                             phase + unc*180.0/np.pi,
                             alpha=0.5, fc='b', label='68% C.I.')
            ax1.set_xlim(frange_plot)
            ax1.set_ylim([-5, 5])
            ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
            ax1.set_xlabel(r'Frequency (Hz)')
            ax1.set_ylabel(r'Phase (meas/model) [deg]')

            for ax in axes.flat:
                ax.grid(which='major', color='black')
                ax.grid(which='minor', ls='--')
                ax.set_xscale('log')
                ax.legend(loc='lower center', ncol=2, handlelength=2)
                ax.axvline(stage_frange_dict[stage][0], ls='--', color='C06')
                ax.axvline(stage_frange_dict[stage][1], ls='--', color='C06')

            ax0.legend(
                handles=plot_handles,
                labels=plot_labels,
                loc='lower left',
            )

            plt.savefig(
                new_report.gen_path(f'actuation_{stage}_{optic}_gpr.png'),
                bbox_inches='tight',
                pad_inches=0.2,
            )
            actuation_gpr_figs.append(fig)

    return actuation_gpr_figs
