# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Jameson Rollins (2021)
#
# This file is part of pyDARM.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.backends.backend_pdf import PdfPages
from . import darm
from scipy.interpolate import interp1d

plt.rcParams.update({'text.usetex': False,
                     'lines.linewidth': 3,
                     'font.family': 'sans-serif',
                     'font.serif': 'Helvetica',
                     'font.size': 10,
                     'xtick.labelsize': 'x-large',
                     'xtick.direction': 'in',
                     'ytick.labelsize': 'x-large',
                     'ytick.direction': 'in',
                     'axes.labelsize': 'medium',
                     'axes.titlesize': 'x-large',
                     'axes.grid': True,
                     'grid.alpha': 0.5,
                     'lines.markersize': 12,
                     'legend.borderpad': 0.2,
                     'legend.fancybox': True,
                     'legend.fontsize': 'medium',
                     'legend.framealpha': 0.7,
                     'legend.handletextpad': 0.1,
                     'legend.labelspacing': 0.2,
                     'legend.loc': 'best',
                     'figure.figsize': (12, 8),
                     'savefig.dpi': 100,
                     'savefig.orientation': 'landscape',
                     'pdf.compression': 9})


class BodePlot:
    """bode plotting object
    """

    def __init__(self, fig=None, title=None, figsize=(12, 8), only='', spspec=[211, 212]):
        """
        Parameters
        ----------
        fig : `object`
            set up object figure
        title : `str`
            title for the bode plot
        figsize : `float` tuple, optional
            figure size, default = (12, 8)
        only : `str`
            if set to 'mag' or 'phase', this object will only
            plot magnitude or phase, and not the usual 2x1 body plot.
        spspec : `int`, optional
            add axes to the figure as part of a subplot arrangement,
            default = [211, 212]
        """
        self.fig = fig or plt.figure(figsize=figsize)
        self.only = only

        self.phase_yticks = np.arange(-180, 180+30, 30)
        self.phase_ylim = (-185, 185)

        if type(spspec) is not list:
            spspec = [spspec]

        # if the figure subplots already exist, respect those instead of
        # creating new ones
        axs = []
        if fig and fig.axes:
            n_spspec = len(spspec)
            if n_spspec == 1:
                ax_idx = self.get_ax_index_from_spspec(spspec[0])
                axs = [fig.axes[ax_idx]]
            elif n_spspec > 2:
                print('Error: expected only 1 or 2 spspec values. '
                      f'{n_spspec} values provided: {spspec}')
            else:
                try:
                    axs = [fig.axes[self.get_ax_index_from_spspec(s)]
                           for s in spspec]
                except Exception:
                    # create new axes since spspec do not exist
                    axs = []
                    for sp in spspec:
                        axs.append(self.fig.add_subplot(sp))

        if self.only == '':
            if axs:
                self.ax_mag, self.ax_phase = axs
            else:
                self.ax_mag = self.fig.add_subplot(spspec[0])
                self.ax_phase = self.fig.add_subplot(spspec[1])

            self.ax_mag.grid(True)
            self.ax_mag.grid(which='major', color='black')
            self.ax_mag.grid(which='minor', linestyle='--')
            self.ax_mag.set_ylabel('Magnitude')

            self.ax_phase.grid(True)
            self.ax_phase.grid(which='minor', linestyle='--')
            self.ax_phase.set_ylabel('Phase [deg]')
            self.ax_phase.set_xlabel('Frequency [Hz]')

        if self.only == 'mag' or self.only == 'magnitude':
            if axs:
                self.ax_mag = axs[0]
            else:
                self.ax_mag = self.fig.add_subplot(spspec[0])
            self.ax_mag.grid(True)
            self.ax_mag.grid(which='minor', axis='both', linestyle='--')
            self.ax_mag.set_ylabel('Magnitude')
            self.ax_mag.set_xlabel('Frequency [Hz]')

        if self.only == 'phase':
            if axs:
                self.ax_phase = axs[0]
            else:
                self.ax_phase = self.fig.add_subplot(spspec[0])
            self.ax_phase = self.fig.add_subplot(111)
            self.ax_phase.grid(True)
            self.ax_phase.grid(which='minor', axis='both', linestyle='--')
            self.ax_phase.set_yticks(self.phase_yticks)
            self.ax_phase.set_ylabel('Phase [deg]')
            self.ax_phase.set_xlabel('Frequency [Hz]')
            self.ax_phase.set_ylim(self.phase_ylim)

        if title:
            self.fig.suptitle(title, y=0.92)

    @staticmethod
    def get_ax_index_from_spspec(spec: int) -> int:
        """Get index of axes object from the spec.

        Assumes a three-digit spec (e.g. 212).
        """
        idx = int(str(spec)[-1]) - 1
        return idx

    def plot(self, freq, tf, **kwargs):
        """add frequency response to plot

        Parameters
        ----------
        freq : `array`, `list`
            frequency array
        tf : `array`, `list`
            frequency response
        **kwargs : `Text` properties
            Other miscellaneous text parameters for matplotlib

        """

        retvals = [None, None]
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            retvals[0], = self.ax_mag.loglog(freq, np.abs(tf), **kwargs)
        if self.only == '' or self.only == 'phase':
            retvals[1], = self.ax_phase.semilogx(freq, np.angle(tf, deg=True),
                                                 **kwargs)
        return retvals

    def error(self, freq, tf, tf_error, **kwargs):
        """add frequency response to plot with error
           Note: Error should be relative.

        Parameters
        ----------
        freq : `array`, `list`
            frequency array
        tf : `array`, `list`
            frequency response
        tf_error : `array`, `list`
            relative error of frequency response
        **kwargs : `Text` properties
            Other miscellaneous text parameters for matplotlib

        """

        retvals = [None, None]
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            errbar_container = self.ax_mag.errorbar(freq, np.abs(tf),
                                                    np.abs(tf)*tf_error, **kwargs)
            self.ax_mag.set_xscale('log')
            self.ax_mag.set_yscale('log')
            retvals[0] = errbar_container
        if self.only == '' or self.only == 'phase':
            errbar_container = self.ax_phase.errorbar(freq,
                                                      np.angle(tf, deg=True),
                                                      tf_error*180/np.pi,
                                                      **kwargs)
            self.ax_phase.set_xscale('log')
            self.ax_phase.set_yscale('linear')
            # self.ax_phase.set_yticks(self.phase_yticks)
            retvals[1] = errbar_container
        return retvals

    def legend(self, labels=None, **kwargs):
        """add legend

        Parameters
        ----------
        labels : `string`, Optional
            add string legend for the plot
        **kwargs : `Text` properties
            Other miscellaneous text parameters for matplotlib
        """

        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            if labels:
                self.ax_mag.legend(labels, **kwargs)

            # labels can also be passed as kwargs to plot,
            # in which case this is fine
            else:
                self.ax_mag.legend(**kwargs)
        if self.only == 'phase':
            if labels:
                self.ax_mag.legend(labels, **kwargs)
            else:
                self.ax_phase.legend(**kwargs)

    def save(self, path):
        """save bode plot to file

        Parameters
        ----------
        path : `str`, `path-like` or `binary file-like`
            path directory for saving the figure

        """

        self.fig.savefig(path)

    def show(self):
        """show interactive plot

        """

        plt.show()

    def xlim(self, freq_min, freq_max):
        """set min max for frequency axis

        Parameters
        ----------
        freq_min : `float`
            start frequency
        freq_max : `float`
            end frequency

        """

        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.set_xlim(freq_min, freq_max)
            self.autoscale_mag_y()
        if self.only == '' or self.only == 'phase':
            self.ax_phase.set_xlim(freq_min, freq_max)

    def ylim(self, mag_min, mag_max, phase_min=-185, phase_max=185):
        """set min max for the magnitude (and phase) axis

        Parameters
        ----------
        mag_min : `float`
            minimum magnitude scale
        mag_max : `float`
            maximum magnitude scale
        phase_min : `float`, Optional
            minimum phase scale, default = -185
        phase_max : `float`, Optional
            maximum phase scale, default = 185

        """

        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.set_ylim(mag_min, mag_max)
        if self.only == '' or self.only == 'phase':
            self.ax_phase.set_ylim(phase_min, phase_max)

    def vlines(self, vfreq, color='red', lw=1.0,
               linestyle='--', label="_nolegend_"):
        """add vertical line at specific frequency in both mag and phase plot

        Parameters
        ----------
        vfreq : `float`
            frequency point for vertical line
        color : `color`, Optional
            color for vertical line, default = 'red'
        lw : `float`
            line width, default = 1.0
        linestyle : {'-', '--', '-.', ':', '', ...}, Optional
            style for vertical line, default = '--'
        label : `str`
            legend string for the vertical line
        """
        retvals = [None, None]
        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            retvals[0] = self.ax_mag.axvline(vfreq, color=color, lw=lw,
                                             linestyle=linestyle, label=label)
        if self.only == '' or self.only == 'phase':
            retvals[1] = self.ax_phase.axvline(vfreq, color=color, lw=lw,
                                               linestyle=linestyle, label=label)
        return retvals

    def text(self, x, y, plot_text):
        """add text in plot

        Parameters
        ----------
        x : `float`
            x-position to place the text
        y : `float`
            y-position to place the text
        plot_text : `str`
            The text
        """

        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.text(x, y, plot_text)
        if self.only == 'phase':
            self.ax_phase.text(x, y, plot_text)

    @staticmethod
    def autoscale_axis(ax, xlim=None, log=False):
        """This function rescales a figure's y-axis.

        Scaling takes place based on the data that is visible given the current
        xlim of the axis, by default. If provided, the data within the provided
        xlim list is used instead.

        Parameters
        ----------
        xlim : list
            data boundary to consider in stead of the entire visible range
        log : bool
            use logarithmic (base 10) scale. Default is False.
        """

        def get_bottom_top(line):
            xd = np.array(line.get_xdata())
            yd = np.array(line.get_ydata())
            lo, hi = xlim if xlim else ax.get_xlim()
            y_disp = yd[((xd > lo) & (xd < hi))]

            minval = np.min(y_disp)
            maxval = np.max(y_disp)
            margin = (maxval - minval) / 4

            top = maxval + margin
            bot = minval - margin

            return bot, top

        lines = ax.get_lines()
        bot, top = np.inf, -np.inf

        for line in lines:
            try:
                new_bot, new_top = get_bottom_top(line)
            except ValueError:
                # skip over non-compliant line objects such as vertical
                # and horizontal lines
                continue
            if new_bot < bot:
                bot = new_bot
            if new_top > top:
                top = new_top

        if log is True:
            yopts = np.array([
                10**np.floor(np.log10(new_bot)),
                10**np.ceil(np.log10(new_bot)),
                10**np.floor(np.log10(new_top)),
                10**np.ceil(np.log10(new_top)),
            ])
        else:
            yopts = np.array([5, 2, 1, 0.5, 0.25, 0.2])

        rt = np.min(top % yopts)
        rb = np.min(bot % yopts)
        v = bot if rb < rt else top
        m = yopts[np.argmin(v % yopts)]
        ysnap_bot = np.floor(bot/m)*m + np.sign(bot)*(bot % m)
        ysnap_top = np.floor(top/m)*m + np.sign(top)*(top % m)
        ax.set_ylim(ysnap_bot, ysnap_top)

    def autoscale_mag_y(self, **kwargs):
        """Rescale the mag plot's y-axis.

        See BodePlot.autoscale_axis() for keyword arguments.
        """

        self.autoscale_axis(self.ax_mag, **kwargs)

    def autoscale_phase_y(self, **kwargs):
        """Rescale the mag plot.

        See BodePlot.autoscale_axis() for keyword arguments.
        """

        self.autoscale_axis(self.ax_phase, **kwargs)

    def greed(self, more_minor=True):
        """add a finer grid than the default

        Parameters
        ----------
        more_minor : `bool`
            Determine the finer tick location for log axes
        """

        if self.only == '' or self.only == 'mag' or self.only == 'magnitude':
            self.ax_mag.yaxis.set_major_locator(
                plticker.LogLocator(base=10, numticks=200))
            if more_minor:
                locmin = plticker.LogLocator(base=10,
                                             subs=(0.1, 0.2, 0.3, 0.4, 0.5,
                                                   0.6, 0.7, 0.8, 0.9),
                                             numticks=6000)
                self.ax_mag.yaxis.set_minor_locator(locmin)
            self.ax_mag.grid(which='major', axis='both', linestyle='-')

        if self.only == '' or self.only == 'phase':
            self.ax_phase.yaxis.set_major_locator(
                plticker.MultipleLocator(base=45))
            self.ax_phase.yaxis.set_minor_locator(
                plticker.MultipleLocator(base=5))
            self.ax_phase.grid(which='major', axis='both', linestyle='-')


def plot(*args, freq_min=0.1, freq_max=5000, freq_points=1001, filename=None,
         mag_min=None, mag_max=None, phase_min=-185, phase_max=185, label=None,
         title=None, style=None, show=None, greed=False, figsize=(12, 8),
         **kwargs):
    """
    This method provides a simple way to plot quickly anything you want.

    Parameters
    ----------
    args : tuple, lists
        Here you can input any kind of transfer function related data.
        It accepts multiple sets in multiple formats.
        FORMATS:
        - 2-tuple (freq,transfer function)
        - 3-tuple (freq,transfer function, rel unc)
        - 4-tuple (freq,transfer function, coherence, rel unc)
        - freq, transfer function (two lists or 1d arrays separated by comma)
        - method that returns a transfer function e.g. D.compute_darm_olg
        (assuming D is a darm model object)
    freq_min : `float`, optional
        start frequency
    freq_max : `float`, optional
        end frequency
    freq_points : `int`, optional
        number of points to calculate
    filename : `str`, optional
        if given, ALL generated graphs will be saved in one pdf.
    mag_min : `float`, optional
        minimum magnitude scale
    mag_max : `float`, optional
        maximum magnitude scale
    phase_min : `float`, optional
        minimum phase scale
    phase_max : `float`, optional
        maximum phase scale
    label : `str` list, optional
        legend string for the data sets given e.g. ['first data', 'second']
    title : `str`, optional
        title of the graph
    style : `str`, optional
        one of the styles matplotlib has or a user filename with style
    show : `bool`, optional
        if true the plot will show
    greed : `bool`, optional
        if true a finer grid is drawn for all figs
    figsize : `float` tuple, optional
        figure size
    **kwargs
        matplotlib arguments passed to all plots

    Returns
    -------
    bp : `pydarm.plot.BodePlot` object
    """

    if filename:
        plt.close('all')
    if style:
        plt.style.use(style)

    # BodyPlot object.
    bp = BodePlot(title=title, figsize=figsize)

    # Temporary index used to identify frequency inputs and transfer function inputs.
    temp_pair_index = 0

    for argument in args:
        # Check if a simple list. If so, then this assumes it is frequency
        # The next one will be taken to be a TF
        if isinstance(argument, (np.ndarray, list)):
            temp_pair_index = temp_pair_index+1
            if (temp_pair_index % 2) == 1:
                # This array should be the frerquency array
                freq_in = argument
            if (temp_pair_index % 2) == 0:
                # This array should then be a TF array
                tf_in = argument
                bp.plot(freq_in, tf_in, **kwargs)
        # Check if this is a tuple. If so, a tuple of size 2 is assumed to
        # be (freq,tf) pair, and if a tuple of size 4 is assumed to be a TF
        # that comes from the measurement class with (freq,tf,coh,unc).
        elif isinstance(argument, (tuple)):
            if len(argument) == 2:
                # This tuple should be (freq,tf)
                freq_in = argument[0]
                tf_in = argument[1]
                bp.plot(freq_in, tf_in, **kwargs)
            elif len(argument) == 3:
                # This tuple should be (freq,tf,unc)
                freq_in = argument[0]
                tf_in = argument[1]
                # Uncertainty is relative, and needs to be for error plot.
                tf_unc = argument[2]
                bp.error(freq_in, tf_in, tf_unc, fmt='ro', linestyle='None', **kwargs)
            elif len(argument) == 4:
                # This tuple should be (freq,tf,coh,unc)
                freq_in = argument[0]
                tf_in = argument[1]
                # tf_coh = argument[2]
                # Uncertainty is relative, and needs to be for error plot.
                tf_unc = argument[3]
                bp.error(freq_in, tf_in, tf_unc, fmt='ro', linestyle='None', **kwargs)
            else:
                raise ValueError('Bad tuple given for plotting')
        else:
            # This argument is a method. We use the frequencies given
            # or the default ones.
            freq = np.logspace(np.log10(float(freq_min)),
                               np.log10(float(freq_max)), int(freq_points))
            tf_in = argument(freq)
            bp.plot(freq, tf_in, **kwargs)

    if label:
        bp.legend(label)
    bp.xlim(freq_min, freq_max)
    if greed:
        bp.greed()
    if mag_min:
        bp.ylim(mag_min, mag_max, phase_min=phase_min, phase_max=phase_max)
    if filename:
        bp.save(filename)
    if show:
        plt.show()
    # Return the handle of the bode plot in case you want to do more things
    # to your plot.
    return bp


def residuals(freq_model, tf_model, freq_data, tf_data, unc_data,
              mag_min=0.8, mag_max=1.2, phase_min=-5, phase_max=5,
              mag_major_tick=0.05, mag_minor_tick=0.01,
              phase_major_tick=2, phase_minor_tick=0.5,
              filename=None, show=None, title=''):
    """
    This method provides a simple way to plot quickly anything you want.

    Parameters
    ----------
    freq_model : `float`, array-like
        frequencies that the model transfer function is computed
    tf_model : `complex`, array-like
        transfer function response values at the `freq_model` points
    freq_data : `float`, array-like
        frequencies that the measured transfer function data values are
        computed at
    tf_data : `complex`, array-like
        measured transfer function response values at the `freq_daata` points
    unc_data : `float`, array-like
        relative uncertainty values, determined from the measurement coherence
    mag_min : `float`, optional
        minimum magnitude scale
    mag_max : `float`, optional
        maximum magnitude scale
    phase_min : `float`, optional
        minimum phase scale
    phase_max : `float`, optional
        maximum phase scale
    mag_major_tick : `float`, optional
        major tick placement for the residual magnitude plot
    mag_minor_tick : `float`, optional
        minor tick placement for the residual magnitude plot
    phase_major_tick : `float`, optional
        major tick placement for the residual phase plot
    phase_minor_tick : `float`, optional
        minor tick placement for the residual phase plot
    filename : `str`, optional
        save the plot to this file
    show : `bool`, optional
        if true the plot will show

    Notes
    -----
    Example usage:
    >>> residuals(freq_model, tf_model,
    ... freq_data, tf_data, unc_data, title='Measurement vs Model')
    """

    # First interpolate the model tf at the frequencies of the data points
    tf_model_interp = np.interp(freq_data, freq_model, tf_model)
    tf_ratio = tf_data/tf_model_interp
    tf_ratio_tuple = freq_data, tf_ratio, unc_data

    qplot = QuadPlot(title=title)
    qplot.plot((freq_data, tf_data, unc_data), tf_ratio_tuple)
    qplot.plot((freq_model, tf_model), ())
    qplot.legend(['Model', 'Data'], ['tl'])

    qplot.yscale('linear', ['tr'])
    qplot.xlim(freq_data[0]*0.9, freq_data[-1]*0.9)

    # Determine a reasonable y scale for mag and phase of residual plot
    mag_ratio_mean = np.mean(np.abs(tf_ratio))
    mag_ratio_std = np.std(np.abs(tf_ratio))
    if (mag_ratio_mean+mag_ratio_std > 1.0) and (mag_ratio_mean-mag_ratio_std < 1.0):
        mag_ratio_mean = 1.0
    qplot.ylim(mag_ratio_mean-mag_ratio_std*2,
               mag_ratio_mean+mag_ratio_std*2, ['tr'])

    phase_ratio_mean = np.mean(np.angle(tf_ratio))*180/np.pi
    phase_ratio_std = np.std(np.angle(tf_ratio))*180/np.pi
    if (phase_ratio_mean+phase_ratio_std > 0.0) and (phase_ratio_mean-phase_ratio_std < 0.0):
        phase_ratio_mean = 0.0
    qplot.ylim(phase_ratio_mean-phase_ratio_std*2,
               phase_ratio_mean+phase_ratio_std*2, ['br'])

    qplot.ax_mag_right.yaxis.set_major_locator(plticker.MultipleLocator(base=mag_major_tick))
    qplot.ax_mag_right.yaxis.set_minor_locator(plticker.MultipleLocator(base=mag_minor_tick))
    qplot.ax_mag_right.grid(which='major', axis='both', linestyle='-')
    qplot.ax_phase_right.yaxis.set_major_locator(plticker.MultipleLocator(base=phase_major_tick))
    qplot.ax_phase_right.yaxis.set_minor_locator(plticker.MultipleLocator(base=phase_minor_tick))
    qplot.ax_phase_right.grid(which='major', axis='both', linestyle='-')
    if show:
        qplot.show()
    if filename:
        qplot.save(filename)


def get_ugf(freq, tf, search_start=5., search_end=1000., n_points=10000):
    """
    Very non-fancy function for easily finding UGF in the simplest of cases.

    Parameters
    ----------
    freq : `float`, `array`
        frequencie arrays corresponding to the given tf
    tf : `complex`, `array`
        transfer function you want the ugf of
    search_start: `float`
        frequency to start UGF search
    search_end: `float`
        frequency to end UGF search
    n_points: `int`
        N point number for increased accuracy of UGF frequency

    Returns
    -------
    floats: ugf frequency, ugf phase, ugf gain, ugf index of original array

    """

    mag = np.abs(tf)
    phase = np.angle(tf)*180/np.pi
    # Interpolate the input TF with a function so that the search comes closer
    # to magnitude=1.
    f_mag = interp1d(freq, mag, kind='cubic', fill_value="extrapolate")
    f_phase = interp1d(freq, phase, kind='cubic', fill_value="extrapolate")
    freq_new = np.logspace(np.log10(search_start), np.log10(search_end), n_points)
    i = 1
    while f_mag(freq_new[i]) > 1 and i < (n_points-1):
        i = i+1

    # The above will return the index i that corresponds to the freq_new array
    # Here we find the index of the original frequency array that is close
    # is close to the UGF.
    temp_mag = np.asarray(mag[freq < search_end])
    idx = (np.abs(temp_mag-1)).argmin()

    if i == n_points-1:
        print('WARNING: UGF NOT FOUND WITHIN THE RANGE GIVEN')
        return -1, 0
    else:
        return freq_new[i], f_phase(freq_new[i]), f_mag(freq_new[i]), idx


def save_multifig(filename, figs=None):
    """method to save all existing (or list of given) figures in one pdf file

    Parameters
    ----------
    filename : `str`
        pdf file name for the figures
    figs : `list`, `dict`
        list of given figures to save
    """

    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()


def critique(*args, filename=None, plot_selection='all', ifo='', show=None,
             label=None, freq_min=0.1, freq_max=5000, freq_points=1001,
             ugf_start=10, ugf_end=1000, greed=True, figsize=(12, 8), **kwargs):
    """
    This method produces critique models for 1 or 2 models.

    Parameters
    ----------
    args : `pydarm.darm.DARMModel` object
        1 or 2 darm models objects, if more than 1, this should be a list
    filename : `str`, optional
        if given, ALL generated graphs will be saved in one pdf
    plot_selection : `str`, optional
        Select plot type, one of: 'all' (default), 'optical', 'actuation',
        'clg', 'olg', or 'digital'
    ifo : `str`, optional
        if given with a model to plot, it will appear in the graph titles
    show : `bool`, optional
        if true the plot(s) will show
    label : `str` list, optional
        a list of labels for legend
    freq_min : `float`, optional
        start frequency
    freq_max : `float`, optional
        final frequency
    freq_points : `int`, optional
        Number of frequency points
    ugf_start : `float`, optional
        start frequency used for the search
    ugf_end : `float`, optional
        end frequency used for the search
    greed : `bool`, optional
    figsize : `float`, tuple
    **kwargs : optional
        Matplotlib values passed to plots
    """
    # See bp1 plot
    default_olg_yspan = 1e12
    # See bp2 plot
    default_olg_zoom_fmin = 10
    default_olg_zoom_fmax = 200
    # See bp3b plot
    default_clg_zoom_fmin = 20
    default_clg_zoom_fmax = 400
    # See bp4 plot
    default_dig_yspan = 1e7
    # See bp6 plot
    default_act_strength_yspan = 1e17
    # See bp8, bp11 plot
    default_act_displ_yspan = 1e17
    if filename:
        plt.close('all')

    # Check if all inputs are darm models. If so, it count the number of
    # models given (1 or 2). If not, it complains.
    if all(isinstance(argument, (darm.DARMModel)) for argument in args):
        if len(args) > 2:
            print('You asked critique plots for more than 2 models. Results might be unpleasant.')
    else:
        ValueError('Function plot.critique only takes DARMModel objects as inputs')

    # Temporary index used to identify the first darm model given.
    temp_model_index = 1
    list_of_figures = []

    plt.rc('legend', fontsize=18)

    for argument in args:
        freq = np.logspace(np.log10(float(freq_min)),
                           np.log10(float(freq_max)), int(freq_points))

        G = argument.compute_darm_olg(freq)
        D = argument.digital.compute_response(freq)
        C = argument.sensing.compute_sensing(freq)
        R = argument.compute_response_function(freq)
        # For all actuation calculations I am using param names that
        # (I think) match old pydarm

        # TF from output of actuation digital filter bank
        # to displacement, for each stage
        x_UIM_strength, x_PUM_strength, x_TST_strength = \
            argument.actuation.xarm.digital_out_to_displacement(freq)
        # TF of suspension digital filters
        x_UIM_umodel, x_PUM_umodel, x_TST_umodel = \
            argument.actuation.xarm.sus_digital_filters_response(freq)
        # TF from LOCK_IN to displacement by stage
        x_UIM_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='UIM')
        x_PUM_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='PUM')
        x_TST_authority = \
            argument.actuation.xarm.compute_actuation_single_stage(freq, stage='TST')
        x_ALL_authority = x_UIM_authority+x_PUM_authority+x_TST_authority
        # TF from DARM_IN to discplacement scaled by optical gain
        x_UIM_total = x_UIM_authority*D*argument.sensing.coupled_cavity_optical_gain
        x_PUM_total = x_PUM_authority*D*argument.sensing.coupled_cavity_optical_gain
        x_TST_total = x_TST_authority*D*argument.sensing.coupled_cavity_optical_gain

        # Relative contribution of actuation stages
        x_UIM_rel = x_UIM_authority*D/R
        x_PUM_rel = x_PUM_authority*D/R
        x_TST_rel = x_TST_authority*D/R
        x_ALL_rel = x_ALL_authority*D/R
        invCnorm = 1/C/R

        if temp_model_index == 1:
            if plot_selection == 'all' or plot_selection == 'olg':
                bp1 = BodePlot(title=f'{ifo} DARM Open Loop Gain: G', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all':
                bp2 = BodePlot(title=f'{ifo} DARM Open Loop Gain: G (ZOOM)', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'clg':
                bp3 = BodePlot(title=f'{ifo} DARM Closed Loop Gain: 1/(1+G)', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp3b = BodePlot(title=f'{ifo} DARM Closed Loop Gain: 1/(1+G) (ZOOM)',
                                figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'digital':
                bp4 = BodePlot(title=f'{ifo} DARM Digital Filter: D', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'optical':
                bp5 = BodePlot(title=f'{ifo} Optical Plant Response: C', figsize=figsize)
                list_of_figures.append(plt.gcf())
            if plot_selection == 'all' or plot_selection == 'actuation':
                bp6 = BodePlot(title=f'{ifo} Act. stage strength', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp7 = BodePlot(title=f'{ifo} Act. stage digital filters', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp8 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ.', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp9 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ. (low zoom)',
                               figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp10 = BodePlot(title=f'{ifo} Act. stage LOCK_IN to Displ. (high zoom)',
                                figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp11 = BodePlot(title=f'{ifo} Act. stage DARM_IN to Disp. (D*A)', figsize=figsize)
                list_of_figures.append(plt.gcf())
                bp12 = BodePlot(title=f'{ifo} Act. stage relative contributions', figsize=figsize,
                                only='magnitude')
                list_of_figures.append(plt.gcf())

        ugf_freq, ugf_phase, ugf_gain, idx = get_ugf(freq, G, search_start=ugf_start,
                                                     search_end=ugf_end)
        phase_margin = 180+ugf_phase

        if plot_selection == 'all' or plot_selection == 'olg':
            bp1.plot(freq, G, **kwargs)
            if label:
                bp1.legend(label)
            bp1.xlim(freq_min, freq_max)
            if greed:
                bp1.greed()
            bp1.vlines(ugf_freq)
            bp1.text(freq_min*1.1, 1.1*10**(-(temp_model_index)),
                     f'UGF {temp_model_index} = {ugf_freq:.2f}Hz, {phase_margin:.2f}deg')
            temp_bottom, temp_top = bp1.ax_mag.get_ylim()
            bp1.ylim(temp_top/default_olg_yspan, temp_top)

        if plot_selection == 'all':
            bp2.plot(freq, G, **kwargs)
            if label:
                bp2.legend(label)
            bp2.xlim(default_olg_zoom_fmin, default_olg_zoom_fmax)
            if greed:
                bp2.greed()
            bp2.vlines(ugf_freq)
            bp2.text(default_olg_zoom_fmin*1.04, 10**((1-temp_model_index)/8),
                     f'UGF {temp_model_index} = {ugf_freq:.2f}Hz, {phase_margin:.2f}deg')

        if plot_selection == 'all' or plot_selection == 'clg':
            bp3.plot(freq, 1./(1.+G), **kwargs)
            bp3b.plot(freq, 1./(1.+G), **kwargs)
            if label:
                bp3.legend(label)
                bp3b.legend(label)
            bp3.xlim(freq_min, freq_max)
            bp3b.xlim(default_clg_zoom_fmin, default_clg_zoom_fmax)
            if greed:
                bp3.greed()
                bp3b.greed()

        if plot_selection == 'all' or plot_selection == 'digital':
            bp4.plot(freq, D, **kwargs)
            if label:
                bp4.legend(label)
            bp4.xlim(freq_min, freq_max)
            if greed:
                bp4.greed()
            temp_bottom, temp_top = bp4.ax_mag.get_ylim()
            bp4.ylim(temp_top/default_dig_yspan, temp_top)

        if plot_selection == 'all' or plot_selection == 'optical':
            bp5.plot(freq, C, **kwargs)
            if label:
                bp5.legend(label)
            bp5.xlim(freq_min, freq_max)
            if greed:
                bp5.greed()

        if plot_selection == 'all' or plot_selection == 'actuation':
            if temp_model_index == 2:
                bp6.plot(freq, x_UIM_strength, ls='--')
                bp6.plot(freq, x_PUM_strength, ls='--')
                bp6.plot(freq, x_TST_strength, ls='--')
            else:
                bp6.plot(freq, x_UIM_strength, **kwargs)
                bp6.plot(freq, x_PUM_strength, **kwargs)
                bp6.plot(freq, x_TST_strength, **kwargs)
                bp6.ax_mag.set_prop_cycle(None)
                bp6.ax_phase.set_prop_cycle(None)
            bp6.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp6.ax_mag.get_ylim()
            bp6.ylim(temp_top/default_act_strength_yspan, temp_top)

            if greed:
                bp6.greed()

            if temp_model_index == 2:
                bp7.plot(freq, x_UIM_umodel, ls='--')
                bp7.plot(freq, x_PUM_umodel, ls='--')
                bp7.plot(freq, x_TST_umodel, ls='--')
            else:
                bp7.plot(freq, x_UIM_umodel, **kwargs)
                bp7.plot(freq, x_PUM_umodel, **kwargs)
                bp7.plot(freq, x_TST_umodel, **kwargs)
                bp7.ax_mag.set_prop_cycle(None)
                bp7.ax_phase.set_prop_cycle(None)
            bp7.xlim(freq_min, freq_max)

            if greed:
                bp7.greed()

            if temp_model_index == 2:
                bp8.plot(freq, x_UIM_authority, ls='--')
                bp8.plot(freq, x_PUM_authority, ls='--')
                bp8.plot(freq, x_TST_authority, ls='--')
                bp8.plot(freq, x_ALL_authority, ls='--')
            else:
                bp8.plot(freq, x_UIM_authority, **kwargs)
                bp8.plot(freq, x_PUM_authority, **kwargs)
                bp8.plot(freq, x_TST_authority, **kwargs)
                bp8.plot(freq, x_ALL_authority, **kwargs)
                bp8.ax_mag.set_prop_cycle(None)
                bp8.ax_phase.set_prop_cycle(None)
            bp8.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp8.ax_mag.get_ylim()
            bp8.ylim(temp_top/default_act_displ_yspan, temp_top)

            if greed:
                bp8.greed()

            if temp_model_index == 2:
                bp9.plot(freq, x_UIM_authority, ls='--')
                bp9.plot(freq, x_PUM_authority, ls='--')
                bp9.plot(freq, x_TST_authority, ls='--')
                bp9.plot(freq, x_ALL_authority, ls='--')
            else:
                bp9.plot(freq, x_UIM_authority, **kwargs)
                bp9.plot(freq, x_PUM_authority, **kwargs)
                bp9.plot(freq, x_TST_authority, **kwargs)
                bp9.plot(freq, x_ALL_authority, **kwargs)
                bp9.ax_mag.set_prop_cycle(None)
                bp9.ax_phase.set_prop_cycle(None)
            bp9.xlim(1e-1, 1e2)

            if greed:
                bp9.greed()

            if temp_model_index == 2:
                bp10.plot(freq, x_UIM_authority, ls='--')
                bp10.plot(freq, x_PUM_authority, ls='--')
                bp10.plot(freq, x_TST_authority, ls='--')
                bp10.plot(freq, x_ALL_authority, ls='--')
            else:
                bp10.plot(freq, x_UIM_authority, **kwargs)
                bp10.plot(freq, x_PUM_authority, **kwargs)
                bp10.plot(freq, x_TST_authority, **kwargs)
                bp10.plot(freq, x_ALL_authority, **kwargs)
                bp10.ax_mag.set_prop_cycle(None)
                bp10.ax_phase.set_prop_cycle(None)
            bp10.xlim(1e2, 1e3)

            if greed:
                bp10.greed()

            if temp_model_index == 2:
                bp11.plot(freq, x_UIM_total, ls='--')
                bp11.plot(freq, x_PUM_total, ls='--')
                bp11.plot(freq, x_TST_total, ls='--')
                bp11.plot(freq, (x_UIM_total+x_PUM_total+x_TST_total), ls='--')
            else:
                bp11.plot(freq, x_UIM_total, **kwargs)
                bp11.plot(freq, x_PUM_total, **kwargs)
                bp11.plot(freq, x_TST_total, **kwargs)
                bp11.plot(freq, (x_UIM_total+x_PUM_total+x_TST_total), **kwargs)
                bp11.ax_mag.set_prop_cycle(None)
                bp11.ax_phase.set_prop_cycle(None)
            bp11.xlim(freq_min, freq_max)
            temp_bottom, temp_top = bp11.ax_mag.get_ylim()
            bp11.ylim(temp_top/default_act_displ_yspan, temp_top)

            if greed:
                bp11.greed()

            if temp_model_index == 2:
                bp12.plot(freq, x_UIM_rel, ls='--')
                bp12.plot(freq, x_PUM_rel, ls='--')
                bp12.plot(freq, x_TST_rel, ls='--')
                bp12.plot(freq, x_ALL_rel, ls='--')
                bp12.plot(freq, invCnorm, ls='--')
            else:
                bp12.plot(freq, x_UIM_rel, **kwargs)
                bp12.plot(freq, x_PUM_rel, **kwargs)
                bp12.plot(freq, x_TST_rel, **kwargs)
                bp12.plot(freq, x_ALL_rel, **kwargs)
                bp12.plot(freq, invCnorm, **kwargs)
                bp12.ax_mag.set_prop_cycle(None)
                # bp12.ax_phase.set_prop_cycle(None)
            bp12.xlim(5, 1000)
            bp12.ylim(1e-3, 4e0)

            if greed:
                bp12.greed()

        if label:
            if plot_selection == 'all' or plot_selection == 'actuation':
                combined_model_label = []
                for labels in label:
                    combined_model_label.append(labels+' UIM')
                    combined_model_label.append(labels+' PUM')
                    combined_model_label.append(labels+' TST')
                bp6.legend(combined_model_label)
                bp7.legend(combined_model_label)
                combined_model_label_tot = []
                for labels in label:
                    combined_model_label_tot.append(labels+' UIM')
                    combined_model_label_tot.append(labels+' PUM')
                    combined_model_label_tot.append(labels+' TST')
                    combined_model_label_tot.append(labels+' Total')
                bp8.legend(combined_model_label_tot)
                bp9.legend(combined_model_label_tot)
                bp10.legend(combined_model_label_tot)
                bp11.legend(combined_model_label_tot)
                combined_model_label_tot = []
                for labels in label:
                    combined_model_label_tot.append(labels+' UIM*D/R')
                    combined_model_label_tot.append(labels+' PUM*D/R')
                    combined_model_label_tot.append(labels+' TST*D/R')
                    combined_model_label_tot.append(labels+' Total')
                    combined_model_label_tot.append(labels+' 1/C')
                bp12.legend(combined_model_label_tot)
        else:
            if plot_selection == 'all' or plot_selection == 'actuation':
                combined_model_label = []
                combined_model_label.append('UIM')
                combined_model_label.append('PUM')
                combined_model_label.append('TST')
                bp6.legend(combined_model_label)
                bp7.legend(combined_model_label)
                combined_model_label_tot = []
                combined_model_label_tot.append('UIM')
                combined_model_label_tot.append('PUM')
                combined_model_label_tot.append('TST')
                combined_model_label_tot.append('Total')
                bp8.legend(combined_model_label_tot)
                bp9.legend(combined_model_label_tot)
                bp10.legend(combined_model_label_tot)
                bp11.legend(combined_model_label_tot)
                combined_model_label_tot = []
                combined_model_label_tot.append('UIM*D/R')
                combined_model_label_tot.append('PUM*D/R')
                combined_model_label_tot.append('TST*D/R')
                combined_model_label_tot.append('Total*D/R')
                combined_model_label_tot.append('1/C')
                bp12.legend(combined_model_label_tot)
        temp_model_index = temp_model_index+1

    if filename:
        save_multifig(filename, list_of_figures)
    if show:
        plt.show()


class QuadPlot:
    """quad bode plotting object
       This is essentially a copy of the BodePlot class but
       plots two bode plots side by side
    """

    def __init__(self, fig=None, title=None, figsize=(12, 8)):
        """
        Parameters
        ----------
        fig : `object`
            object figure
        title : `str`
            put a text for the plot title
        figsize : `(float, float)`
            width, height in inches for the figure size
        """
        self.fig = fig or plt.figure(figsize=figsize)

        self.ax_mag_left = self.fig.add_subplot(221)
        self.ax_mag_left.grid(True)
        self.ax_mag_left.grid(which='minor', axis='both', linestyle='--')
        # self.ax_mag_left.axhline(1, color='k', linestyle='dashed')
        self.ax_mag_left.set_ylabel('Magnitude')

        self.ax_phase_left = self.fig.add_subplot(223)
        self.ax_phase_left.grid(True)
        self.ax_phase_left.grid(which='minor', axis='both', linestyle='--')
        self.ax_phase_left.set_yticks(np.arange(-180, 180+30, 30))
        self.ax_phase_left.set_ylabel('Phase [deg]')
        self.ax_phase_left.set_xlabel('Frequency [Hz]')
        self.ax_phase_left.set_ylim(-185, 185)

        self.ax_mag_right = self.fig.add_subplot(222)
        self.ax_mag_right.grid(True)
        self.ax_mag_right.grid(which='minor', axis='both', linestyle='--')
        # self.ax_mag_right.axhline(1, color='k', linestyle='dashed')
        self.ax_mag_right.set_ylabel('Magnitude')

        self.ax_phase_right = self.fig.add_subplot(224)
        self.ax_phase_right.grid(True)
        self.ax_phase_right.grid(which='minor', axis='both', linestyle='--')
        self.ax_phase_right.set_yticks(np.arange(-180, 180+30, 30))
        self.ax_phase_right.set_ylabel('Phase [deg]')
        self.ax_phase_right.set_xlabel('Frequency [Hz]')
        self.ax_phase_right.set_ylim(-185, 185)

        if title:
            self.fig.suptitle(title, y=0.93)

    def plot(self, tuple_left, tuple_right, **kwargs):
        """Add frequency response to plot with or without error
           Note: Error should be relative.

        Parameters
        ----------
        tuple_left : `tuple`, `array-like`
            add frequency response for the left-side frequencies area
        tuple_right : `tuple`, `array-like`
            add frequency response for the right-side frequencies area
        **kwargs : `Text` properties
            Other miscellaneous text parameters for matplotlib
        """
        if len(tuple_left) == 2:
            freq_left, tf_left = tuple_left
            self.ax_mag_left.loglog(freq_left, np.abs(tf_left), **kwargs)
            self.ax_phase_left.semilogx(freq_left, np.angle(tf_left, deg=True), **kwargs)
        elif len(tuple_left) == 3:
            freq_left, tf_left, error_left = tuple_left
            self.ax_mag_left.errorbar(freq_left, np.abs(tf_left),
                                      np.abs(tf_left)*error_left, fmt='o', linestyle='None',
                                      markersize=6, **kwargs)
            self.ax_mag_left.set_xscale('log')
            self.ax_mag_left.set_yscale('log')
            self.ax_phase_left.errorbar(freq_left, np.angle(tf_left, deg=True),
                                        error_left*180/np.pi, fmt='o', linestyle='None',
                                        markersize=6, **kwargs)
            self.ax_phase_left.set_xscale('log')
            self.ax_phase_left.set_yscale('linear')
        elif len(tuple_left) == 0:
            'Do nothing'
        else:
            ValueError('Input tuples expected to be length 2 or 3')

        if len(tuple_right) == 2:
            freq_right, tf_right = tuple_right
            self.ax_mag_right.semilogx(freq_right, np.abs(tf_right), **kwargs)
            self.ax_phase_right.semilogx(freq_right, np.angle(tf_right, deg=True), **kwargs)
        elif len(tuple_right) == 3:
            freq_right, tf_right, error_right = tuple_right
            self.ax_mag_right.errorbar(freq_right, np.abs(tf_right),
                                       np.abs(tf_right)*error_right, fmt='o', linestyle='None',
                                       **kwargs)
            self.ax_mag_right.set_xscale('log')
            self.ax_mag_right.set_yscale('log')
            self.ax_phase_right.errorbar(freq_right, np.angle(tf_right, deg=True),
                                         error_right*180/np.pi, fmt='o', linestyle='None',
                                         **kwargs)
            self.ax_phase_right.set_xscale('log')
            self.ax_phase_right.set_yscale('linear')
        elif len(tuple_right) == 0:
            'Do nothing'
        else:
            ValueError('Input tuples expected to be length 2 or 3')

    def legend(self, label=None, quadrant=['tl', 'bl', 'tr', 'br']):
        """add legend

        Parameters
        ----------
        label : `str`
            add text label for legend
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select position for legend on specific quadrant
            'tl' : top-left (magnitude left)
            'bl' : bottom-left (phase left)
            'tr' : top-right (magnitude right)
            'br' : bottom-right (phase right)
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
            select position for legend on specific quadrant
            1 : top-left (magnitude left)
            3 : bottom-left (phase left)
            2 : top-right (magnitude right)
            4 : bottom-right (phase right)
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.legend(label)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.legend(label)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.legend(label)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.legend(label)

    def save(self, path):
        """save bode plot to file

        Parameters
        ----------
        path : `str`, `path-like`
            path directory for saving the figure
        """
        self.fig.savefig(path)

    def show(self):
        """show interactive plot"""
        plt.show()

    def xlim(self, freq_min, freq_max, quadrant=['tl', 'bl', 'tr', 'br']):
        """set min max for frequency axis

        Parameters
        ----------
        freq_min : `float`, Optional
            start frequency
        freq_max : `float`, Optional
            final frequency
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to setup xlim
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.set_xlim(freq_min, freq_max)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.set_xlim(freq_min, freq_max)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.set_xlim(freq_min, freq_max)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.set_xlim(freq_min, freq_max)

    def ylim(self, y_min, y_max, quadrant=['tl', 'bl', 'tr', 'br']):
        """set min max for the magnitude (and phase) axis

        Parameters
        ----------
        freq_min : `float`, Optional
            start frequency
        freq_max : `float`, Optional
            final frequency
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to setup ylim
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]

        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.set_ylim(y_min, y_max)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.set_ylim(y_min, y_max)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.set_ylim(y_min, y_max)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.set_ylim(y_min, y_max)

    def vlines(self, vfreq, quadrant=['tl', 'bl', 'tr', 'br']):
        """add vertical line at specific frequency in both mag and phase plot

        Parameters
        ----------
        vfreq : `float`
            frequency position for vertical line
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to add vertical line
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.axvline(vfreq, color='red', lw=1.0, linestyle='--',
                                     label='_nolegend_')
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.axvline(vfreq, color='red', lw=1.0, linestyle='--',
                                       label='_nolegend_')
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_phase_right.axvline(vfreq, color='red', lw=1.0, linestyle='--',
                                        label='_nolegend_')
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.axvline(vfreq, color='red', lw=1.0, linestyle='--',
                                        label='_nolegend_')

    def text(self, x, y, plot_text, quadrant=['tl', 'bl', 'tr', 'br']):
        """add text in plot

        Parameters
        ----------
        x : `float`
            x-position to place the text
        y : `float`
            y-position to place the text
        plot_text : `str`
            The text
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to add the text
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.text(x, y, plot_text)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.text(x, y, plot_text)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.text(x, y, plot_text)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.text(x, y, plot_text)

    def xscale(self, scale='linear', quadrant=['tl', 'bl', 'tr', 'br']):
        """change the y scale of plot at given quadrant, linear or log

        Parameters
        ----------
        scale : `str`, Optional
            scale for x axis, default='linear'
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to set the xscale
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.set_xscale(scale)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.set_xscale(scale)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.set_xscale(scale)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.set_xscale(scale)

    def yscale(self, scale='linear', quadrant=['tl', 'bl', 'tr', 'br']):
        """change the y scale of plot at given quadrant, linear or log

        Parameters
        ----------
        scale : `str`, Optional
            scale for y axis, default='linear'
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to set the yscale
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.set_yscale(scale)
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.set_yscale(scale)
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.set_yscale(scale)
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.set_yscale(scale)

    def greed(self, more_minor=True, quadrant=['tl', 'bl', 'tr', 'br']):
        """add a finer grid than the default

        Parameters
        ----------
        more_minor : `bool`, Optional
            set a finer grid on the plot, default=True
        quadrant : ['tl', 'bl', 'tr', or 'br']
            select specific plot to set finer grid
            alternatively you can use a list of numbers
            quadrant : [1, 3, 2, or 4]
        """
        if ('tl' in quadrant) or (1 in quadrant):
            self.ax_mag_left.yaxis.set_major_locator(plticker.LogLocator(base=10, numticks=200))
            if more_minor:
                locmin = plticker.LogLocator(base=10,
                                             subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
                                             numticks=6000)
                self.ax_mag_left.yaxis.set_minor_locator(locmin)
            self.ax_mag_left.grid(which='major', axis='both', linestyle='-')
        if ('bl' in quadrant) or (3 in quadrant):
            self.ax_phase_left.yaxis.set_major_locator(plticker.MultipleLocator(base=45))
            self.ax_phase_left.yaxis.set_minor_locator(plticker.MultipleLocator(base=5))
            self.ax_phase_left.grid(which='major', axis='both', linestyle='-')
        if ('tr' in quadrant) or (2 in quadrant):
            self.ax_mag_right.yaxis.set_major_locator(plticker.LogLocator(base=10, numticks=200))
            if more_minor:
                locmin = plticker.LogLocator(base=10,
                                             subs=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
                                             numticks=6000)
                self.ax_mag_right.yaxis.set_minor_locator(locmin)
            self.ax_mag_right.grid(which='major', axis='both', linestyle='-')
        if ('br' in quadrant) or (4 in quadrant):
            self.ax_phase_right.yaxis.set_major_locator(plticker.MultipleLocator(base=45))
            self.ax_phase_right.yaxis.set_minor_locator(plticker.MultipleLocator(base=5))
            self.ax_phase_right.grid(which='major', axis='both', linestyle='-')
