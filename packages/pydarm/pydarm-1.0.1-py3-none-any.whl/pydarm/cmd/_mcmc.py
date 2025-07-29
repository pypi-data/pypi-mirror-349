from copy import deepcopy

import corner
import numpy as np
from matplotlib.colors import colorConverter
from matplotlib.patches import Patch as mplpatches
from matplotlib.lines import Line2D


def sensing_MCMC(report):
    """run sensing MCMC

    Writes out resulting map and chains files to the report directory.

    """
    report = deepcopy(report)

    config = report.config['Sensing']
    processed_sensing, meas_timestamp = report.measurements['Sensing']

    # FIXME: if a previous MCMC run exists for a measurement
    # that has matching run-time parameters (num steps, burn in,
    # and freq region) then use those results here instead of
    # re-running the MCMC here.
    priors_bound = np.array(config['params']['priors_bound'])
    if np.all(priors_bound == None):  # noqa: E711
        priors_bound = None

    processed_sensing.run_mcmc(
        fmin=config['params']['mcmc_fmin'],
        fmax=config['params']['mcmc_fmax'],
        priors_bound=priors_bound,
        burn_in_steps=config['params']['mcmc_burn_in'],
        steps=config['params']['mcmc_steps'],
        save_chain_to_file=report.gen_path(
            'sensing_mcmc_chain.hdf5'),
        save_map_to_file=report.gen_path(
            'sensing_mcmc_map.json'),
    )


def actuation_MCMC(report):
    """generate actuation MCMC

    Writes out resulting map and chains files to the report directory.

    """
    report = deepcopy(report)

    for stage, optics in report.config['Actuation'].items():
        if stage == 'params':
            continue

        for optic, config in optics.items():
            if optic == 'params':
                continue

            name = f'Actuation/{stage}/{optic}'

            processed_actuation, meas_timestamp = report.measurements[name]

            # FIXME: if a previous MCMC run exists for a measurement
            # that has matching run-time parameters (num steps, burn in,
            # and freq region) then use those results here instead of
            # re-running the MCMC here.
            priors_bound = np.array(config['params']['priors_bound'])
            if np.all(priors_bound == None):  # noqa: E711
                priors_bound = None

            processed_actuation.run_mcmc(
                fmin=config['params']['mcmc_fmin'],
                fmax=config['params']['mcmc_fmax'],
                priors_bound=priors_bound,
                burn_in_steps=config['params']['mcmc_burn_in'],
                steps=config['params']['mcmc_steps'],
                save_chain_to_file=report.gen_path(
                    f'actuation_{stage}_{optic}_mcmc_chain.hdf5'
                ),
                save_map_to_file=report.gen_path(
                    f'actuation_{stage}_{optic}_mcmc_map.json'
                ),
            )


def print_mcmc_params(chain, mcmcParams, quantileLevels):
    '''
    This function is just for printing MCMC parameters for easy copy/pasting
    to alog. Update of Jeff's existing code for prettier formatting.

    Prints in two formats: first the quantile values,
    then in the format 'X (+Y/-Z)'.

    Parameters
    ----------
    mcmcParams: dict
        Keys should be parameter names, values include quantiles, errbars, labels
        TODO improve documentation

    Returns
    -------
    tableQuant: str
        Printable table of values in quantile format
    tablePM: str
        Printable table of values in +/- format

    '''

    chain = np.transpose(deepcopy(chain))
    for i, param in enumerate(mcmcParams.values()):
        quantiles = corner.quantile(
            chain[i],
            quantileLevels)
        param['median'] = quantiles[1]
        param['errplus'] = quantiles[2] - quantiles[1]
        param['errminus'] = quantiles[1] - quantiles[0]
        param['quantiles'] = quantiles

    # Set up lists to hold the tables (will be joined with newline later)
    tableQuant = []
    tablePM = []

    # Define a column spacer
    spacer = " | "

    # Set up left column width for parameter labels
    ncharsLabel = max([len(p['label']) for p in mcmcParams.values()])

    # Set up widths for the quantiles section
    ncharsCol = max([len(f"{x:4.4g}") for p in mcmcParams.values()
                    for x in p['quantiles']])

    # Set up the header for the quantiles section
    tag = "(quantile)"
    pline = [f"{'Parameter':<{ncharsLabel-len(tag)}s}{tag}"]
    for x in quantileLevels:
        pline += [f"{str(x):<{ncharsCol}s}"]
    header = spacer.join(pline)
    tableQuant += [header]
    tableQuant += ["-"*len(header)]

    # Set up each line for the quantiles section
    for param in mcmcParams.values():
        pline = [f"{param['label']:<{ncharsLabel}s}"]
        for x in param['quantiles']:
            valstr = f"{x:4.4g}"
            pline += [f"{valstr:<{ncharsCol}s}"]
        tableQuant += [spacer.join(pline)]
    tableQuant += ["-"*len(header)]

    # Set up column widths for the +/- section
    ncharsCol = max([len(f"{param[key]:4.4g} ({abs(param[key]/param['median']*100):.2f}%)")
                    for param in mcmcParams.values()
                    for key in ['median', 'errplus', 'errminus']])

    # Set up head for the +/- section
    tag = "(value +/-)"
    pline = [f"{'Parameter':<{ncharsLabel-len(tag)}s}{tag}"]
    for x in ["value", " +", " -"]:
        pline += [f"{str(x):<{ncharsCol}s}"]
    header = spacer.join(pline)
    tablePM += [header]
    tablePM += ["-"*len(header)]

    # Set up each line for the +/- section
    for param in mcmcParams.values():
        pline = [f"{param['label']:<{ncharsLabel}s}"]
        for key in ['median', 'errplus', 'errminus']:
            if key == 'median':
                fmat = f"{param[key]:4.4g}"
            else:
                fmat = f"{param[key]:4.4g} ({(param[key]/param['median']*100):.2f}%)"
            pline += [f"{fmat:<{ncharsCol}s}"]
        tablePM += [spacer.join(pline)]

    tablePM = "\n".join(tablePM)
    tableQuant = "\n".join(tableQuant)

    return tableQuant, tablePM


def make_corner_plot(
        chain, mcmcparams, math_labels,
        quantilelevels, outfile, title,
):
    '''
    Make an MCMC corner plot
    parameters
    ----------
    chain: 2d array
        size: (number of steps in mcmc chain),(number of parameters)

    mcmcparams: dict
        keys should be parameter names, values include quantiles, errbars, labels

    math_labels: list
        labels for corner plot

    quantilelevels: 1d array

    outfile
        path to save corner plot

    title
        plot title

    returns
    -------
    none
        just saves figures
    '''

    color = 'C3'  # base fill color for contours
    truthcolor = 'C0'  # color for median markers
    nbins = 100  # number of bins for histogram

    # === create main plot
    # we copy the following from its definition in
    # https://github.com/dfm/corner.py/blob/e65dd4cdeb7a9f7f75cbcecb4f07a07de65e2cea/src/corner/core.py
    # and take only first 3 levels
    levels = 1.0 - np.exp(-0.5 * np.arange(0.5, 2.1, 0.5) ** 2)[0:3]
    # NOTE: in at least one previous script the following levels were used:
    # levels = (1 - np.exp(-1. / 2.), 1 - np.exp(- 4. / 2.), 1 - np.exp(-9 / 2.))

    cp = corner.corner(
        chain,
        bins=nbins,
        quantiles=quantilelevels,
        smooth=2.0,
        labels=math_labels,
        verbose=False,
        label_kwargs={'fontsize': 10},
        show_titles=True,
        title_fmt='.3e',
        title_kwargs={'fontsize': 12, 'loc': 'left'},
        plot_datapoints=False,
        plot_density=True,
        plot_contours=True,
        fill_contours=True,
        color=color,
        use_math_text=True,
        levels=levels,
        max_n_ticks=5,
        truths=list(mcmcparams['map'].values()),
        truth_color=truthcolor
    )
    suptitle = cp.suptitle(title, fontsize=20)

    text_bbox = suptitle.get_tightbbox(renderer=cp.canvas.get_renderer())
    text_height = text_bbox.y1-text_bbox.y0
    fig_height = cp.get_size_inches()[1]*cp.dpi
    adjust_fraction = text_height/fig_height*2

    # ==== reproducing the contour colors
    # annoying as this is, corner does not provide a way to get
    # the contour fill color maps, nor the default levels.
    rgba_color = colorConverter.to_rgba(color)
    contour_cmap = [list(rgba_color) for lev in levels] + [rgba_color]
    for i, l in enumerate(levels):
        contour_cmap[i][-1] *= float(i) / (len(levels) + 1)
    contour_cmap = contour_cmap[1:][::-1]

    # === generating custom legend

    # shaded rectangle for each contour fill color
    legend_symbols = [mplpatches(
        facecolor=contour_cmap[i],
        edgecolor=contour_cmap[i]) for i in range(len(contour_cmap))]
    # line for the "truth" values (mcmcparam median values)
    legend_symbols.append(Line2D([0], [0], color=truthcolor, lw=3))
    # empty rectangle to make space for bin count label
    legend_symbols.append(mplpatches(alpha=0))

    # create legend
    cp.legend(
        legend_symbols,
        [r'$1\sigma$',
         r'$2\sigma$',
         r'$3\sigma$',
         'map',
         f'({nbins} bins for 1d pdf)'],
        fontsize=15,
        title_fontsize=15,
        title="2d pdf contours",
        frameon=True,
        markerscale=20.0,
    )

    # === fix up the histogram axes

    # grab all subplot axes
    axes = cp.get_axes()

    for ax in axes:
        ax.set_aspect(1/ax.get_data_ratio())  # force plots to be square
        ax.yaxis.offsetText.set_fontsize(10)  # adjust the "x 10^n" label size
        ax.xaxis.offsetText.set_fontsize(10)

    cp.subplots_adjust(wspace=.1, hspace=.1, top=(1-adjust_fraction))

    # determine which axes belong to the rightside histograms
    nparams = len(mcmcparams['map'].values())
    length_sides = np.arange(nparams)
    histogram_indices = (nparams+1)*length_sides

    # create rightside axis for each histogram
    for i in histogram_indices:
        ax = axes[i]
        ax.yaxis.set_label_position('right')
        ax.set_ylabel('1d norm. pdf \n (percent per bin)', fontsize=10)

    # resize the tick params to make them smaller
    for ax in axes:
        ax.tick_params(axis='both', labelsize=10)

    # save figure
    cp.set_size_inches(10, 10)
    cp.savefig(outfile)
    return cp
