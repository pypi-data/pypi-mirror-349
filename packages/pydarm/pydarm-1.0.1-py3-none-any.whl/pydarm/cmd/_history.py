from copy import deepcopy

import numpy as np
from scipy.signal import freqresp
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from ._log import CMDError
from ._const import FREE_PARAM_LABEL_MAP
from ._mcmc import (
    print_mcmc_params,
    make_corner_plot,
)
from ..utils import read_chain_from_hdf5
from ..sensing import SensingModel
from ..plot import BodePlot


def adjust_phase_yticks(ax, maxsteps=7):
    """A quick and somewhat ugly fix for adjusting the phase axis to the best
    step size from a list of 'neat' step sizes.
    """
    ps = np.array([30, 20, 15, 10, 5, 2, 1, .1, .01])  # possible step sizes
    ymin, ymax = ax.get_ylim()
    step = ps[max(np.searchsorted((ymax-ymin)/ps, maxsteps)-1, 0)]
    loc_major = MultipleLocator(base=step)
    loc_minor = MultipleLocator(base=step/5)
    ax.yaxis.set_major_locator(loc_major)
    ax.yaxis.set_minor_locator(loc_minor)


def adjust_mag_yticks(ax, maxsteps=7):
    """A quick and somewhat ugly fix for adjusting the phase axis to the best
    step size from a list of 'neat' step sizes.
    """
    ps = np.array([10, 5, 2, 1, 0.9, 0.5, 0.2, 0.1, 0.05, 0.01])  # possible step sizes
    ymin, ymax = ax.get_ylim()
    step = ps[max(np.searchsorted((ymax-ymin)/ps, maxsteps)-1, 0)]
    loc_major = MultipleLocator(base=step)
    loc_minor = MultipleLocator(base=step/5)
    ax.yaxis.set_major_locator(loc_major)
    ax.yaxis.set_minor_locator(loc_minor)


def sensing_history(new_report, epoch_reports, ref_report):
    """generate sensing history plots

    """
    new_report = deepcopy(new_report)
    epoch_reports = deepcopy(epoch_reports)

    config = new_report.config['Sensing']
    C_new = new_report.model.sensing
    C_ref = ref_report.model.sensing

    # calculate reference optical response
    C_ref_optical_response = SensingModel.optical_response(
        C_ref.coupled_cavity_pole_frequency,
        C_ref.detuned_spring_frequency,
        C_ref.detuned_spring_q,
        C_ref.is_pro_spring,
    )

    processed_sensing, timestamp = new_report.measurements['Sensing']

    # Get the common frequency axis and measurement info
    frequencies, measOpticalResponse, measOpticalResponseUnc = \
        processed_sensing.get_processed_measurement_response()

    angular_frequencies = 2*np.pi*frequencies

    refNormOpticalResponse = freqresp(
        C_ref_optical_response,
        angular_frequencies
    )[1]

    refOpticalResponse = refNormOpticalResponse * \
        C_ref.coupled_cavity_optical_gain

    # === Plotting setup
    xlim = [5, 1400]
    # Set up common title names
    tfp_title = "Optical response transfer functions\n(scaled by 1/$C_R$)"
    rp_title = "Optical response residuals\n(measurement/model)"
    subtitleText = f"All fixed parameters drawn from {new_report.model_file}"
    sp_titlesize = 12

    # sensing history figure
    sensing_hist_fig = plt.figure()
    sensing_hist_fig.suptitle(f"{new_report.IFO} sensing model history"
                              " (last 9 measurements)\n", fontsize=20
                              )
    sensing_hist_fig.text(
        .5, .93,
        subtitleText,
        in_layout=True,
        horizontalalignment='center',
        transform=sensing_hist_fig.transFigure)

    # transfer function plot
    sensing_hist_tf_bode = BodePlot(fig=sensing_hist_fig, spspec=[221, 223])
    sensing_hist_tf_bode.ax_mag.set_title(tfp_title, fontsize=sp_titlesize)

    # residuals plot
    sensing_hist_res_bode = BodePlot(fig=sensing_hist_fig, spspec=[222, 224])
    sensing_hist_res_bode.ax_mag.set_title(rp_title, fontsize=sp_titlesize)

    figs = []
    sensing_hist_handles = []
    sensing_hist_labels = []

    # Compute the optical response based on MCMC parameters
    mcmc_params = new_report.get_sens_mcmc_results()
    mcmc_map = mcmc_params['map']

    mcmcNormOpticalResponse = freqresp(
        SensingModel.optical_response(
            mcmc_map['Fcc'],
            mcmc_map['Fs'],
            mcmc_map['Qs'],
            C_new.is_pro_spring),
        angular_frequencies)[1]

    mcmcOpticalResponse = mcmcNormOpticalResponse * \
        mcmc_map['Hc'] * \
        np.exp(
            -2*np.pi*1j*mcmc_map['tau_C'] *
            frequencies)

    # Select scaling for the history plot
    expscale = int(np.floor(np.log10(C_ref.coupled_cavity_optical_gain)))
    yscale_str = f"x $10^{{{expscale}}}$" if expscale else ''
    ax_mag = sensing_hist_tf_bode.ax_mag
    ax_mag.set_ylabel(f'Magnitude (ct/m) {yscale_str}')
    scale = 10**expscale

    # Add reference model curve
    resp = mcmcOpticalResponse / scale
    sensing_hist_model_handle, _ = sensing_hist_tf_bode.plot(frequencies,
                                                             resp, zorder=1)
    sensing_hist_model_label = f"{ref_report.id} model"
    sensing_hist_handles.append(sensing_hist_model_handle)
    sensing_hist_labels.append(sensing_hist_model_label)

    # add new_report measurement
    meas_optgain_err, _ = sensing_hist_tf_bode.error(frequencies,
                                                     measOpticalResponse/scale,
                                                     measOpticalResponseUnc,
                                                     fmt='.',
                                                     zorder=25)
    meas_optgain_label = f"{timestamp} measurement"
    sensing_hist_handles.append(meas_optgain_err)
    sensing_hist_labels.append(meas_optgain_label)

    # Add a null curve to keep the color-coding consistent on the
    # residuals plot
    sensing_hist_res_bode.plot([], [])
    vline, _ = sensing_hist_tf_bode.vlines(
        config['params']['mcmc_fmin'],
        color='black', lw=2)
    sensing_hist_tf_bode.vlines(config['params']['mcmc_fmax'], color='black',
                                lw=2)
    vline_label = (f"MCMC Fit Range: {config['params']['mcmc_fmin']} Hz"
                   f" to {config['params']['mcmc_fmax']} Hz")

    meas_model, fmin, fmax, measurement, chain = read_chain_from_hdf5(
        new_report.gen_path('sensing_mcmc_chain.hdf5')
    )

    # Set up the quantile levels
    quantileLevels = np.array([0.16, 0.5, 0.84])

    # Make corner plot
    # FIXME: this is a terrible workaround for our label mapping problem
    keylist = ['Hc', 'Fcc', 'Fs', 'Qs', 'tau_C']
    math_labels = [FREE_PARAM_LABEL_MAP[x]['mathlabel'] for x in keylist]
    corner_fig = make_corner_plot(
        chain,
        mcmc_params,
        math_labels,
        quantileLevels,
        new_report.gen_path(
            "sensing_mcmc_corner.png"
        ),
        f"{timestamp} sensing function\nMCMC corner plot"
    )

    # We need an additional figure for the MCMC results comparison.
    # Setup is in the same format as the multi-measurement comparison.
    fig_mcmc = plt.figure()
    fig_mcmc.suptitle(f"{new_report.IFO} sensing model MCMC summary\n", fontsize=20)
    fig_mcmc.text(
        .5, .93,
        subtitleText,
        in_layout=True,
        horizontalalignment='center',
        transform=fig_mcmc.transFigure)

    tfp_mcmc = BodePlot(fig=fig_mcmc, spspec=[221, 223])
    tfp_mcmc.ax_mag.set_title(tfp_title, fontsize=sp_titlesize)
    tfp_mcmc.ax_mag.set_ylabel(f'Magnitude (ct/m) x $10^{{{expscale}}}$')
    rp_mcmc = BodePlot(fig=fig_mcmc, spspec=[222, 224])
    rp_mcmc.ax_mag.set_title(rp_title, fontsize=sp_titlesize)

    # Add the curves to the plot
    ref_resp_line, _ = tfp_mcmc.plot(
        frequencies,
        refOpticalResponse/scale)
    ref_resp_line_label = \
        f"Model w free params from report {ref_report.id}"

    mcmc_resp_line, _ = tfp_mcmc.plot(
        frequencies,
        mcmcOpticalResponse/scale)
    mcmc_resp_line_label = ("Model w free params from MCMC"
                            f"\nfit to {timestamp} data")

    meas_err_containers, _ = tfp_mcmc.error(
        frequencies,
        measOpticalResponse/scale,
        measOpticalResponseUnc,
        fmt='.',
        markersize=5)
    meas_err_containers_label = f"{timestamp} measurement"

    rp_mcmc.error(
        frequencies,
        measOpticalResponse/refOpticalResponse,
        measOpticalResponseUnc,
        fmt='.')
    rp_mcmc.error(
        frequencies,
        measOpticalResponse/mcmcOpticalResponse,
        measOpticalResponseUnc,
        fmt='.')
    rp_mcmc.ax_mag.set_yscale('linear')
    rp_mcmc.ax_mag.set_ylim(0.9, 1.1)
    rp_mcmc.ax_mag.set_xlim(*xlim)
    rp_mcmc.ax_phase.set_xlim(*xlim)
    rp_mcmc.ax_phase.set_ylim(-10, 10)
    adjust_phase_yticks(rp_mcmc.ax_phase)
    rp_mcmc.ax_phase.yaxis.set_minor_locator(MultipleLocator(1))
    rp_mcmc.ax_mag.yaxis.set_minor_locator(MultipleLocator(.01))
    tfp_mcmc.ax_phase.set_ylim(-180, 180)
    tfp_mcmc.ax_phase.yaxis.set_minor_locator(MultipleLocator(30))
    tfp_mcmc.ax_mag.set_xlim(*xlim)
    tfp_mcmc.ax_phase.set_xlim(*xlim)

    # Add vertical lines marking the fit range for the MCMC
    vline_label = f"Fit range: [{fmin:0.2f}, {fmax:0.2f}] Hz"
    for p in [tfp_mcmc, rp_mcmc]:
        v_line = p.vlines(
            fmin, color='k', lw=2,
        )
        p.vlines(fmax, color='k', lw=2)

    fig_mcmc.legend(
        handles=[
            meas_err_containers[0],
            ref_resp_line,
            mcmc_resp_line,
            v_line[0]
            ],
        labels=[
            meas_err_containers_label,
            ref_resp_line_label,
            mcmc_resp_line_label,
            vline_label
            ],
        bbox_to_anchor=(.1, .82, .8, .1),
        loc='lower left',
        ncol=3,
        mode='expand',
        fontsize='small',
        markerscale=1,
        bbox_transform=fig_mcmc.transFigure
    )

    # setup params to print table
    table_params = {k: v for (k, v) in
                    FREE_PARAM_LABEL_MAP.items() if k in
                    ['Hc', 'Fcc', 'Fs', 'Qs', 'tau_C']
                    }
    _, mcmcTablePM = print_mcmc_params(chain,
                                       table_params, (.16, .5, .84))
    fig_mcmc.tight_layout(rect=(0, 0, 1, .91))
    tbox = fig_mcmc.text(
        .5, 0,
        "\n"*6+mcmcTablePM+"\n",
        fontfamily='monospace',
        size=10,
        horizontalalignment='center',
        verticalalignment='bottom',
        transform=fig_mcmc.transFigure,
    )

    text_bbox = tbox.get_tightbbox(
        renderer=fig_mcmc.canvas.get_renderer())
    text_height = text_bbox.y1-text_bbox.y0
    fig_height = fig_mcmc.get_size_inches()[1]*fig_mcmc.dpi
    adjust_fraction = (text_height)/fig_height
    fig_mcmc.subplots_adjust(bottom=adjust_fraction)
    fig_mcmc.set_size_inches(10, 10)
    fig_mcmc.savefig(
        new_report.gen_path(
            "sensing_mcmc_compare.png"
        ),
    )
    figs.append(fig_mcmc)
    figs.append(corner_fig)
    # Add meas curves to residuals plot
    sensing_hist_res_bode.error(
        frequencies,
        measOpticalResponse/mcmcOpticalResponse,
        measOpticalResponseUnc,
        fmt='.',
        zorder=25)
    sensing_hist_res_bode.ax_mag.set_yscale('linear')
    sensing_hist_res_bode.ax_mag.set_ylim(0.9, 1.1)
    sensing_hist_res_bode.ax_phase.set_ylim(-15, 15)
    adjust_phase_yticks(sensing_hist_res_bode.ax_phase)

    for im, ireport in enumerate(epoch_reports):
        processed_sensing, timestamp = ireport.measurements['Sensing']

        # Get the common frequency axis and measurement info
        frequencies, measOpticalResponse, measOpticalResponseUnc = \
            processed_sensing.get_processed_measurement_response()

        angular_frequencies = 2*np.pi*frequencies

        mcmcNormOpticalResponse = freqresp(
            SensingModel.optical_response(
                mcmc_map['Fcc'],
                mcmc_map['Fs'],
                mcmc_map['Qs'],
                ireport.model.sensing.is_pro_spring),
            angular_frequencies)[1]

        mcmcOpticalResponse = mcmcNormOpticalResponse * \
            mcmc_map['Hc'] * \
            np.exp(
                -2*np.pi*1j*mcmc_map['tau_C'] *
                frequencies)

        # Add meas curves to transfer function comparison plots
        sensing_hist_err_container, _ = sensing_hist_tf_bode.error(
            frequencies,
            measOpticalResponse/scale,
            measOpticalResponseUnc,
            fmt='.',
            zorder=20-im)
        sensing_hist_tf_bode_label = f"{ireport.id} measurement"
        sensing_hist_handles.append(sensing_hist_err_container)
        sensing_hist_labels.append(sensing_hist_tf_bode_label)

        # Add meas curves to residuals plot
        sensing_hist_res_bode.error(
            frequencies,
            measOpticalResponse/mcmcOpticalResponse,
            measOpticalResponseUnc,
            fmt='.',
            zorder=20-im)
        sensing_hist_res_bode.ax_mag.set_yscale('linear')
        sensing_hist_res_bode.ax_mag.set_ylim(0.9, 1.1)
        sensing_hist_res_bode.ax_phase.set_ylim(-15, 15)
        adjust_phase_yticks(sensing_hist_res_bode.ax_phase)

    sensing_hist_tf_bode.ax_phase.yaxis.set_major_locator(MultipleLocator(45))
    sensing_hist_tf_bode.ax_phase.set_ylim(-180, 180)
    sensing_hist_tf_bode.ax_mag.set_xlim(*xlim)
    sensing_hist_tf_bode.ax_phase.set_xlim(*xlim)
    sensing_hist_res_bode.ax_mag.set_xlim(*xlim)
    sensing_hist_res_bode.ax_phase.set_xlim(*xlim)
    sensing_hist_handles.append(vline)
    sensing_hist_labels.append(vline_label)
    sensing_hist_fig.tight_layout(rect=(0, 0, 1, .95))
    sensing_hist_fig.legend(
        handles=sensing_hist_handles,
        labels=sensing_hist_labels,
        bbox_to_anchor=(.05, .83, .9, .1),
        loc='lower left',
        ncol=3,
        mode='expand',
        fontsize='small',
        markerscale=1,
        bbox_transform=sensing_hist_fig.transFigure,
    )
    figs.append(sensing_hist_fig)

    # Wrap up and save figure
    sensing_hist_fig.savefig(
        new_report.gen_path(
            "sensing_tf_history.png"
        )
    )
    return figs


def actuation_history(new_report, epoch_reports, ref_report):
    """generate actuation history plots

    """
    new_report = deepcopy(new_report)
    epoch_reports = deepcopy(epoch_reports)

    base_config = new_report.config['Actuation']
    epoch_act = ref_report.model.actuation

    # Set up common title names
    tfp_title = "Actuation strength transfer functions\n(scaled by $H_{ref}$)"
    rp_title = "Actuation strength residuals\n(meas./model w. free params)"
    subtitle_text = f"All fixed parameters drawn from {new_report.model_file}"
    sp_titlesize = 12

    xlim = [5, 1300]
    xscale_range = [10, 100]  # x-axis range to consider when scaling y-axis
    figs = []

    # process by actuator stage
    mcmc_params = new_report.get_act_mcmc_results()
    for stage, optics in base_config.items():
        if stage == 'params':
            continue

        for optic, config in optics.items():
            if optic == 'params':
                continue

            # main figure
            act_hist_fig = plt.figure()
            act_hist_fig.suptitle(
                f"{new_report.IFO}SUS{optic}"
                f" {stage} actuation model history (last 9 measurements)\n",
                fontsize=20)
            act_hist_fig.text(
                .5, .93,
                subtitle_text,
                horizontalalignment='center',
                transform=act_hist_fig.transFigure)

            # transfer function plot (comparison)
            tfp_hist_act = BodePlot(fig=act_hist_fig, spspec=[221, 223])
            tfp_hist_act.ax_mag.set_title(tfp_title, fontsize=sp_titlesize)

            # residuals plot (comparison)
            rp_hist_act = BodePlot(fig=act_hist_fig, spspec=[222, 224])
            rp_hist_act.ax_mag.set_title(rp_title, fontsize=sp_titlesize)

            # use actuation model from report at the last epoch boundary
            # as the reference
            epoch_act_arm = getattr(epoch_act, f'{optic[-1].lower()}arm')

            # gain_units, gain_to_NpCt_factor
            if stage == 'L1':
                actuator_strength_param = abs(epoch_act_arm.uim_npa)
                gain_units = 'N/A'
            elif stage == 'L2':
                actuator_strength_param = abs(epoch_act_arm.pum_npa)
                gain_units = 'N/A'
            elif stage == 'L3':
                actuator_strength_param = abs(epoch_act_arm.tst_npv2)
                gain_units = '$N/V^2$'
            else:
                raise CMDError(f"unknown stage in config: {stage}")

            # process new_report measurement
            act_hist_handles = []
            act_hist_labels = []
            name = f'Actuation/{stage}/{optic}'
            processed_actuation_new, timestamp = new_report.measurements[name]

            # Get the common frequency axis and measurement info
            frequencies, meas_actuator_strength, meas_actuator_strength_unc = \
                processed_actuation_new.get_processed_measurement_response()

            # N/A or N/V**2, as taken from current ini
            actuator_strength = actuator_strength_param * np.ones(
                frequencies.shape)

            # Select scaling for the plot
            expscale = int(np.floor(np.log10(actuator_strength_param)))
            scale = 10**expscale
            scale_text = f"x $10^{{{expscale}}}$" if expscale else ''
            hist_ylabel_text = f'Magnitude [{gain_units} {scale_text}]'

            # Add reference model curve
            model_handle, _ = tfp_hist_act.plot(frequencies,
                                                actuator_strength/scale,
                                                zorder=1)
            model_label = f"{ref_report.id} model"
            act_hist_handles.append(model_handle)
            act_hist_labels.append(model_label)

            # Add a null curve to keep the color-coding consistent
            # to the residuals plot
            rp_hist_act.plot([], [])

            meas_model, fmin, fmax, measurement, chain = read_chain_from_hdf5(
                new_report.gen_path(f'actuation_{stage}_{optic}_mcmc_chain.hdf5')
            )

            # Set up the quantile levels
            quantileLevels = np.array([0.16, 0.5, 0.84])

            # get mcmc params for this stage + optic configuration
            act_unit_params = mcmc_params['/'.join([stage, optic])]

            # Make corner plot
            # Determine which parameters labels are present and which math
            # labels
            # are associated
            math_labels = [FREE_PARAM_LABEL_MAP[x]['mathlabel'] for x in
                           [stage, 'tau_A']]
            corner_fig = make_corner_plot(
                chain,
                act_unit_params,
                math_labels,
                quantileLevels,
                new_report.gen_path(
                    f"actuation_{stage}_{optic}_mcmc_corner.png"
                ),
                f"{timestamp} {optic} {stage} actuation\nMCMC corner plot"
            )

            mcmc_actuator_strength = \
                act_unit_params['map']['H_A'] \
                * np.exp(-2*np.pi*1j
                         * act_unit_params['map']['tau_A']
                         * frequencies)

            fig_mcmc_handles = []
            fig_mcmc_labels = []
            fig_mcmc = plt.figure()
            fig_mcmc.suptitle(
                f"{new_report.IFO}SUS{optic} {stage} "
                "actuation model MCMC summary\n",
                fontsize=20)
            fig_mcmc.text(
                .5, .93,
                subtitle_text,
                in_layout=True,
                horizontalalignment='center',
                transform=fig_mcmc.transFigure)

            tfp_mcmc_act = BodePlot(fig=fig_mcmc, spspec=[221, 223])
            tfp_mcmc_act.ax_mag.set_title(tfp_title, fontsize=sp_titlesize)
            tfp_mcmc_act.ax_mag.set_ylabel(f'Mag. [{gain_units} {scale_text}]')
            rp_mcmc_act = BodePlot(fig=fig_mcmc, spspec=[222, 224])
            rp_mcmc_act.ax_mag.set_title(rp_title, fontsize=sp_titlesize)

            mcmc_model_free_line, _ = tfp_mcmc_act.plot(frequencies,
                                                        actuator_strength/scale)
            model_label = f"Model w free params from report {ref_report.id}"
            fig_mcmc_handles.append(mcmc_model_free_line)
            fig_mcmc_labels.append(model_label)

            # plot actuation from mcmc fit
            mcmc_model_fit_line, _ = tfp_mcmc_act.plot(frequencies,
                                                       mcmc_actuator_strength/scale)
            mcmc_model_fit_label = ("Model w free params from"
                                    f"\nMCMC fit to {timestamp} data")
            fig_mcmc_handles.append(mcmc_model_fit_line)
            fig_mcmc_labels.append(mcmc_model_fit_label)

            mcmc_model_meas_handle, _ = tfp_mcmc_act.error(
                frequencies,
                meas_actuator_strength/scale,
                meas_actuator_strength_unc,
                fmt='.',
                zorder=20)
            mcmc_model_meas_label = f"{timestamp} measurement"
            fig_mcmc_handles.append(mcmc_model_meas_handle)
            fig_mcmc_labels.append(mcmc_model_meas_label)

            rp_mcmc_act.error(
                frequencies,
                meas_actuator_strength/actuator_strength,
                meas_actuator_strength_unc,
                label=(
                    f"{timestamp} meas / model w free params\n"
                    f" from MCMC fit to {timestamp}"),
                fmt='.')
            rp_mcmc_act.error(
                frequencies,
                meas_actuator_strength/mcmc_actuator_strength,
                meas_actuator_strength_unc,
                label=(
                    f"{timestamp} meas / model w free params\n"
                    f" from report {new_report.id}"),
                fmt='.')

            rp_mcmc_act.ax_mag.set_yscale('linear')
            tfp_mcmc_act.ax_mag.set_yscale('linear')

            rp_mcmc_act.ax_phase.set_ylim(-10, 10)
            rp_mcmc_act.autoscale_mag_y(xlim=xscale_range)
            rp_mcmc_act.ax_mag.set_xlim(*xlim)
            rp_mcmc_act.ax_phase.set_xlim(*xlim)

            tfp_mcmc_act.autoscale_mag_y(xlim=xscale_range, log=True)
            tfp_mcmc_act.autoscale_phase_y(xlim=xscale_range)
            tfp_mcmc_act.ax_mag.set_xlim(*xlim)
            tfp_mcmc_act.ax_phase.set_xlim(*xlim)

            adjust_mag_yticks(tfp_mcmc_act.ax_mag)
            adjust_mag_yticks(rp_mcmc_act.ax_mag)
            adjust_phase_yticks(rp_mcmc_act.ax_phase)
            adjust_phase_yticks(tfp_mcmc_act.ax_phase)

            # Add vertical lines marking the fit range for the MCMC
            for p in [tfp_mcmc_act, rp_mcmc_act]:
                mcmc_vline_handle, _ = p.vlines(
                    config['params']['mcmc_fmin'], color='k', lw=2)
                p.vlines(config['params']['mcmc_fmax'], color='k', lw=2)
            mcmc_vline_label = (f"Fit range {config['params']['mcmc_fmin']} to"
                                f" {config['params']['mcmc_fmax']} Hz")

            fig_mcmc_handles.append(mcmc_vline_handle)
            fig_mcmc_labels.append(mcmc_vline_label)

            fig_mcmc.tight_layout(rect=(0, 0, 1, .95))
            fig_mcmc.legend(
                handles=fig_mcmc_handles,
                labels=fig_mcmc_labels,
                bbox_to_anchor=(.05, .84, .9, .1),
                loc='lower left',
                ncol=3,
                mode='expand',
                fontsize='small',
                markerscale=1,
                bbox_transform=fig_mcmc.transFigure
            )

            table_params = {k: v for (k, v) in
                            FREE_PARAM_LABEL_MAP.items() if k in
                            [stage, 'tau_A']
                            }
            _, mcmcTablePM = print_mcmc_params(chain,
                                               table_params, (.16, .5, .84))
            tbox = fig_mcmc.text(
                .5, 0,
                "\n"*6+mcmcTablePM+"\n",
                fontfamily='monospace',
                size=10,
                horizontalalignment='center',
                verticalalignment='bottom',
                transform=fig_mcmc.transFigure,
            )

            text_bbox = tbox.get_tightbbox(
                renderer=fig_mcmc.canvas.get_renderer())
            text_height = text_bbox.y1-text_bbox.y0
            fig_height = fig_mcmc.get_size_inches()[1]*fig_mcmc.dpi
            adjust_fraction = (text_height)/fig_height
            fig_mcmc.subplots_adjust(bottom=adjust_fraction)
            fig_mcmc.savefig(
                new_report.gen_path(
                    f"actuation_{stage}_{optic}_mcmc_compare.png"),
            )
            figs.append(fig_mcmc)
            figs.append(corner_fig)

            # add new_report to history plot
            # Add meas curves to transfer function comparison plots
            act_hist_err_container, _ = tfp_hist_act.error(
                frequencies,
                meas_actuator_strength/scale,
                meas_actuator_strength_unc,
                fmt='.',
                zorder=25)
            act_hist_err_label = f"{timestamp} measurement"
            act_hist_handles.append(act_hist_err_container)
            act_hist_labels.append(act_hist_err_label)

            # Add meas curves to residuals plot
            rp_hist_act.error(
                frequencies,
                meas_actuator_strength/actuator_strength,
                meas_actuator_strength_unc,
                fmt='.',
                zorder=25)

            # ==== Loop over measurement dates/times
            for im, ireport in enumerate(epoch_reports):
                processed_actuation, timestamp = ireport.measurements[name]

                # Get the common frequency axis and measurement info
                frequencies, meas_actuator_strength, unc = \
                    processed_actuation.get_processed_measurement_response()
                meas_actuator_strength_unc = unc

                actuator_strength = actuator_strength_param * np.ones(
                    frequencies.shape)

                # Add meas curves to transfer function comparison plots
                act_hist_err_container, _ = tfp_hist_act.error(
                    frequencies,
                    meas_actuator_strength/scale,
                    meas_actuator_strength_unc,
                    fmt='.',
                    zorder=20-im)
                act_hist_err_label = f"{timestamp} measurement"
                act_hist_handles.append(act_hist_err_container)
                act_hist_labels.append(act_hist_err_label)

                # Add meas curves to residuals plot
                rp_hist_act.error(
                    frequencies,
                    meas_actuator_strength/actuator_strength,
                    meas_actuator_strength_unc,
                    fmt='.',
                    zorder=20-im)

            tfp_hist_act.ax_mag.set_yscale('linear')
            tfp_hist_act.autoscale_mag_y(xlim=xscale_range, log=True)
            tfp_hist_act.autoscale_phase_y(xlim=xscale_range)
            tfp_hist_act.ax_mag.set_ylabel(hist_ylabel_text)
            tfp_hist_act.ax_mag.set_xlim(*xlim)
            tfp_hist_act.ax_phase.set_xlim(*xlim)

            rp_hist_act.ax_mag.set_yscale('linear')
            rp_hist_act.autoscale_mag_y(xlim=xscale_range)
            rp_hist_act.autoscale_phase_y(xlim=xscale_range)
            rp_hist_act.ax_mag.set_xlim(*xlim)
            rp_hist_act.ax_phase.set_xlim(*xlim)

            adjust_mag_yticks(tfp_hist_act.ax_mag)
            adjust_phase_yticks(tfp_hist_act.ax_phase)
            adjust_phase_yticks(rp_hist_act.ax_phase)
            adjust_mag_yticks(rp_hist_act.ax_mag)

            # nasty hack to avoid plotting issues when there is only
            # one report to process
            if not ref_report == new_report:
                figs.append(act_hist_fig)

            # add mcmc fit range to hist
            act_hist_vline, _ = tfp_hist_act.vlines(config['params']['mcmc_fmin'], lw=2,
                                                    color='k')
            tfp_hist_act.vlines(config['params']['mcmc_fmax'], lw=2, color='k')
            rp_hist_act.vlines(config['params']['mcmc_fmin'], lw=2, color='k')
            rp_hist_act.vlines(config['params']['mcmc_fmax'], lw=2, color='k')
            act_hist_handles.append(act_hist_vline)
            act_hist_labels.append("MCMC Fit Range: "
                                   f"{config['params']['mcmc_fmin']:0.0f} Hz "
                                   f"to {config['params']['mcmc_fmax']:0.0f}"
                                   " Hz")

            act_hist_fig.tight_layout(rect=(0, 0, 1, .95))
            act_hist_fig.legend(
                handles=act_hist_handles,
                labels=act_hist_labels,
                bbox_to_anchor=(.05, .83, .9, .1),
                loc='lower left',
                ncol=3,
                mode='expand',
                fontsize='small',
                markerscale=1,
                bbox_transform=act_hist_fig.transFigure
            )

            # Wrap up and save figure
            act_hist_fig.savefig(
                new_report.gen_path(
                    f"actuation_{stage}_{optic}_tf_history.png"
                )
            )
    return figs
