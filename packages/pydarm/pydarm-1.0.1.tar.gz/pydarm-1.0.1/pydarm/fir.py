# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Aaron Viets (2021)
#               Miftahul Ma'arif (2021)
#
# This file is part of pyDARM.

import numpy as np
from scipy import signal, fft
import os
import h5py
import warnings
from copy import deepcopy
from .firtools import (DPSS, resample,
                       DolphChebyshev, Blackman, freqresp,
                       two_tap_zero_filter_response)
from .plot import plot
from .model import Model
from .darm import DARMModel
from .calcs import CALCSModel


class FIRfilter(object):
    """
    Model parameters for FIR filter creation

    Parameters
    ----------
    fNyq : `int`, optional
        Nyquist frequency of FIR filter
    dur : `float`, optional
        Duration in seconds of FIR filter
    highpass_fcut : `float`, optional
        Cut off frequency for high-pass filter
    lowpass_fcut : `float`, optional
        Cut off frequency for low-pass filter (relevant for inverse sensing filter)
    window_type : `str`, optional
        Type of window function to use. Options are 'dpss', 'kaiser',
        'dolph_chebyshev', and 'hann'.
    freq_res: `float`, optional
        Frequency resolution of the FIR filter, computed as half the width of

    Returns
    -------
    FIRfilter : list
        List of model parameters for FIR filter creation parameters

    """
    def __init__(self, fNyq=8192, desired_dur=1.0, highpass_fcut=None, lowpass_fcut=None,
                 window_type='dpss', freq_res=3.0):
        self.figs = []
        self.fNyquist = fNyq
        self.window_type = window_type
        self.desired_dur = desired_dur
        self.highpass_fcut = highpass_fcut
        self.lowpass_fcut = lowpass_fcut
        self.freq_res = freq_res

        # Set up remaining FIR params
        self._params()
        # Set up window functions
        self._generate_window()

    def _params(self):
        """ Define attributes derived from user parameters """
        self.dt = 1/(2.0*self.fNyquist)
        self.dur = self._compute_duration()
        self.latency = self.dur/2.0
        if self.window_type == 'hann':
            warnings.warn("Frequency resolution can not be set independently"
                          "of duration since you are using Hann window.")
            self.freq_res = 2.0 / self.dur
        self.df = 1.0 / self.dur
        self.freq_array = np.fft.rfftfreq(int(self.dur / self.dt), d=self.dt)
        if self.df != self.freq_array[1] - self.freq_array[0]:
            raise ValueError("Desired frequency resolution is %f"
                             "but actual frequency resolution is %f"
                             % self.df, (self.freq_array[1] - self.freq_array[0]))
        if self.highpass_fcut:
            self.samples_to_HPcorner = int((self.highpass_fcut - 0.75 * self.freq_res) / self.df)
        else:
            self.samples_to_HPcorner = 0
        if self.lowpass_fcut:
            self.samples_to_LPcorner = int((self.fNyquist - self.lowpass_fcut) / self.df)
        else:
            self.samples_to_LPcorner = 0
        self.delay_samples = round(self.latency / self.dt)
        self.delay_array = \
            np.exp(-2 * np.pi * 1j * self.freq_array * self.delay_samples * self.dt)
        self.advance_array = \
            np.exp(2 * np.pi * 1j * self.freq_array * self.delay_samples * self.dt)

    def _compute_duration(self):
        """ Compute filter duration in units of seconds """
        nsamples = round(self.desired_dur / self.dt)
        exact_dur = nsamples * self.dt
        return exact_dur

    def _generate_window(self):
        """ Compute a window function so that the filter falls off smoothly at
            the edges """
        length = int(self.dur / self.dt)
        if self.window_type == "dpss":
            alpha = self.freq_res * length * self.dt
            alpha = np.sqrt(alpha * alpha - 1)
            dpss = DPSS(length, alpha, max_time=1)
            self.window = dpss
        elif self.window_type == "kaiser":
            alpha = self.freq_res * length * self.dt
            beta = np.pi * np.sqrt(alpha * alpha - 1)
            kaiserwin = signal.windows.kaiser(length,
                                              int(beta))
            self.window = kaiserwin
        elif self.window_type == "dolph_chebyshev":
            alpha = self.freq_res * length * self.dt
            alpha = np.sqrt(1.37 * 1.37 * alpha * alpha - 1)
            DC = DolphChebyshev(length, alpha)
            self.window = DC
        elif self.window_type == "blackman":
            blackmanwin = Blackman(length)
            self.window = blackmanwin
        elif self.window_type == "hann":
            hannwin = np.hanning(np.float64(length))
            self.window = hannwin
        else:
            raise ValueError("Window type needs to be set to 'dpss', 'kaiser', "
                             "'dolph_chebyshev' or 'hann'. It is currently ", self.window_type, ".")

    def _smooth_model(self, model):
        """ Use a tapered cosine function to smooth (roll-off) the model below
            the desired cutoff frequency """
        smooth_samples = int((self.highpass_fcut - 0.4 * self.freq_res) / self.df)
        slope = model[smooth_samples - 1] - model[smooth_samples]
        model[:smooth_samples] = model[smooth_samples - 1] \
            + slope * smooth_samples / np.pi * 2 * np.cos(np.arange(smooth_samples)
                                                          * np.pi / 2 / smooth_samples)

    def _highpass(self, model, upsample_factor):
        """Apply a half-hann window highpass filter to the model above the
           desired cutoff frequency"""
        hp_hann = np.hanning(2*upsample_factor)[:upsample_factor]
        hp_hann = np.concatenate((np.zeros(upsample_factor * self.samples_to_HPcorner
                                           - len(hp_hann)), hp_hann))
        model[:upsample_factor * self.samples_to_HPcorner] *= hp_hann

    def _lowpass(self, model, upsample_factor):
        """Apply a half-hann window lowpass filter to the model below the
           desired cutoff frequency"""
        lp_hann = np.hanning(2 * upsample_factor * self.samples_to_LPcorner)
        lp_hann = lp_hann[-upsample_factor * self.samples_to_LPcorner:]
        model[-upsample_factor * self.samples_to_LPcorner:] *= lp_hann

    def create_fir_filter(self, static_model, save_to_file=None):
        """
        Generate an FIR filter based on provided frequency-domain model

        Parameters
        ----------
        static_model : array-like
            Transfer function of frequency domain model
        save_to_file : `str`, optional
            Filename (NPZ) to save the data from this result

        Returns
        -------
        model_FIR : `float64`, array-like
            A time domain FIR filter model
        double_model : `float`, array-like
            An array of real doubles FIR filter model

        """
        model = np.asarray(static_model, dtype=np.complex128)

        if self.highpass_fcut:
            # Smooth off the model below the cutoff
            self._smooth_model(model)

        # Upsample for better FFT quality
        upsample_factor = 16
        model = resample(model, upsample_factor * (len(model) - 1) + 1, return_double=True)

        if self.highpass_fcut:
            # Create a high-pass filter to be convolved with the FIR model filter
            self._highpass(model, upsample_factor)

        if self.lowpass_fcut:
            # Create a low-pass filter to be convolved with the FIR model filter
            self._lowpass(model, upsample_factor)

        # Zero out the Nyquist component
        model[-1] = 0

        # Take inverse real FFT of model
        model_FIR = fft.irfft(model)

        # Add delay to model to make sure it falls off at the edges
        model_FIR = np.roll(model_FIR, int(self.latency / self.dt))[:len(model_FIR)
                                                                    // upsample_factor]
        freq_array = np.fft.rfftfreq(len(model_FIR), d=self.dt)
        if not np.array_equal(freq_array, self.freq_array):
            print("Frequency arrays for FIR and model don't agree!")
            print("Freq array from FIR filter is ", freq_array)
            print("Freq array from model is ", self.freq_array)

        # Apply a window so that the filter falls off smoothly at the edges.
        model_FIR *= self.window

        # Convert the filter model into an array of real doubles
        # so that it can be read into gstlal_compute_strain
        double_model = np.zeros(2 * len(model))
        double_model[::2] = np.real(model)
        double_model[1::2] = np.imag(model)

        if save_to_file is not None:
            np.savez(save_to_file, model_FIR=np.float64(model_FIR),
                     double_model=double_model)

        return np.float64(model_FIR), double_model

    def check_td_vs_fd(self, tdfilt, fdmodel, filename="td_vs_fd.png",
                       plot_title="Frequency Response", legend=[r'FIR filter', r'DARM model'],
                       samples_per_lobe=8, ymax_increase=1):
        """
        Checking time-domain vs frequency-domain filters

        Parameters
        ----------
        tdfilt :
            array of time domain filter
        fdmodel :
            array of frequency domain model
        filename :
            str for filename for plot output
        plot_title :
            str for title of plot
        legend :
            str, array-like for plot legend titles
        samples_per_lobe :
            int for factor to upsample by for finer
            frequency resolution
        ymax_increase :
            int for factor above max y array value
            to display in plot

        Returns
        -------
        plot of filter and model comparison
        freq_array:
            frequency array for comparison
        mag_ratio:
            array of magnitude comparison
        phase_diff:
            array of phase differences

        """
        # Find the frequency response of the FIR filter at the requested frequency resolution
        fd_from_td = freqresp(tdfilt, delay_samples=self.delay_samples,
                              samples_per_lobe=samples_per_lobe)
        Nf = len(fd_from_td)

        # Check the frequency-domain model to see if it is sampled correctly
        Nfdmodel = len(fdmodel)
        if Nfdmodel != Nf:
            long_fdmodel = resample(fdmodel, Nf)
        else:
            long_fdmodel = fdmodel

        long_fdmodel[0] = long_fdmodel[1]
        ratio = fd_from_td / long_fdmodel

        df = float(self.fNyquist) / (Nf - 1)
        freq_array = np.arange(0.0, self.fNyquist + df, df)

        fd_from_td_mag = np.absolute(fd_from_td)
        fd_from_model_mag = np.absolute(long_fdmodel)
        mag_ratio = np.absolute(ratio)

        phase_diff = np.angle(ratio) * 180 / np.pi

        ymin = pow(10, int(round(np.log10(fd_from_td_mag[int(np.ceil(1.0 / self.df))]))) - 2)
        ymax = pow(10, int(round(np.log10(fd_from_model_mag[int(np.ceil(1.0 / self.df))]))) + 2)
        ymax *= ymax_increase
        bp = plot(freq_array[:len(fd_from_td)], fd_from_td,
                  freq_array[:len(long_fdmodel)], long_fdmodel, freq_min=1,
                  freq_max=max(self.freq_array), mag_min=ymin, mag_max=ymax,
                  label=legend,
                  title=r'%s' % plot_title.replace('_', '\\_'),
                  filename=filename)
        self.figs.append(bp.fig)
        bp_ratio = plot(freq_array[:len(ratio)], ratio, freq_min=1,
                        freq_max=max(self.freq_array),
                        label="Filter / model",
                        title=r'Ratio of %s' % plot_title.replace('_', '\\_'),
                        filename=filename.split('.png')[0]+"_ratio.png")
        self.figs.append(bp_ratio.fig)
        bp_ratio_10hz = plot(freq_array[:len(ratio)], ratio, freq_min=10,
                             freq_max=max(self.freq_array),
                             label="Filter / model",
                             mag_min=0.90, mag_max=1.10,
                             phase_min=-10, phase_max=10,
                             title=r'Ratio of %s (above 10 Hz)' % plot_title.replace('_', '\\_'),
                             filename=filename.split('.png')[0]+"_ratio_above10Hz.png")
        self.figs.append(bp_ratio_10hz.fig)
        return freq_array, mag_ratio, phase_diff


class FIRFilterFileGeneration(DARMModel):
    """ FIR filter file generation. """
    def __init__(self, config, fir_config=None):
        """
        Initialize a FIRFilterFileGeneration object

        Note that any string or path-to-file string
        in `FIR` will override anything in the `config`
        parameter string or path-to-file

        Parameters
        ----------
        config : file path or string
            INI config
        fir_config : file path or string, optional
            INI config
        """
        super().__init__(config)
        if 'FIR' in self._config:
            self.FIR = Model(config, measurement='FIR')
        if fir_config is not None:
            self.FIR = Model(fir_config, measurement='FIR')
        if not hasattr(self, 'FIR'):
            raise ValueError('No FIR parameters have been defined')

        # Load model parameters
        self.calcs = CALCSModel(config)

        # Parameters directly from IFO params file
        self._load_ifo_sensing_params()

        # Calibration line frequencies
        self._store_calib_line_freqs()

        # Frequency vector for models of A, D, C, and R
        self.model_freqs = np.arange(0, 8192.25, 0.25)

        # Compute models to store in the filters
        self._compute_fd_cal_models()

        # Compute pcal correction factors at line frequencies provided
        if hasattr(self.FIR, 'endstation'):
            endstation = self.FIR.endstation
        else:
            endstation = True
        if hasattr(self.FIR, 'include_dewhitening'):
            include_dewhitening = self.FIR.include_dewhitening
        else:
            include_dewhitening = True
        self._compute_pcal_corrs(endstation, include_dewhitening)

        # Store EPICS records. Ref LIGO-T1700106-v10 and LIGO-P2100107
        self._compute_epics(endstation)

        self.figs = []

        # Set up list of attributes to exclude from filters file
        self.exclude_from_filters = ['_config', 'measurement', 'run',
                                     'model_date', 'start', 'end', 'cal_data_root',
                                     'name', 'sensing', 'actuation', 'digital',
                                     'pcal', 'FIR', 'calcs', 'figs', 'exclude_from_filters',
                                     'coupled_cavity']

    def _load_ifo_sensing_params(self):
        """Extract and store parameters for the sensing
           function from the CALCS IFO model"""
        self.arm_length = self.calcs.sensing.mean_arm_length()
        self.fcc = self.calcs.sensing.coupled_cavity_pole_frequency
        self.fs = self.calcs.sensing.detuned_spring_frequency
        self.fs_squared = np.real(pow(self.fs, 2.0))
        self.srcQ = self.calcs.sensing.detuned_spring_q
        self.ips = self.calcs.sensing.is_pro_spring
        self.coupled_cavity = self.calcs.sensing.optical_response(
                                  self.fcc,
                                  self.fs,
                                  self.srcQ,
                                  pro_spring=self.ips)

    def _store_calib_line_freqs(self):
        """Extract calibration line frequencies to store in class
           in order to save these in the final filters file"""
        self.src_pcal_line_freq = self.calcs.calcs.cal_line_sus_pcal_frequency
        self.ka_pcal_line_freq = self.calcs.calcs.cal_line_sus_pcal_frequency
        self.kc_pcal_line_freq = self.calcs.calcs.cal_line_sens_pcal_frequency
        self.ktst_esd_line_freq = self.calcs.calcs.cal_line_sus_tst_frequency
        self.pum_act_line_freq = self.calcs.calcs.cal_line_sus_pum_frequency
        self.uim_act_line_freq = self.calcs.calcs.cal_line_sus_uim_frequency
        self.high_pcal_line_freq = self.calcs.calcs.cal_line_high_pcal_frequency
        if hasattr(self.FIR, 'roaming_pcal_line_freq'):
            self.roaming_pcal_line_freq = self.FIR.roaming_pcal_line_freq

    def _pcal_corr_real_and_imag(self, freq, endstation, include_dewhitening):
        """Compute the real and imaginary parts of PCal corrections"""
        pcal_corr = self.calcs.pcal.compute_pcal_correction(np.asarray([freq]),
                                                            endstation=endstation,
                                                            include_dewhitening=include_dewhitening)
        pcal_corr_re = np.real(pcal_corr)
        pcal_corr_im = np.imag(pcal_corr)
        return pcal_corr_re, pcal_corr_im

    def _compute_pcal_corrs(self, endstation, include_dewhitening):
        """Compute PCal corrections at specifed frequencies."""
        self.ka_pcal_corr_re, self.ka_pcal_corr_im = self._pcal_corr_real_and_imag(
                                                          self.ka_pcal_line_freq,
                                                          endstation,
                                                          include_dewhitening)
        self.kc_pcal_corr_re, self.kc_pcal_corr_im = self._pcal_corr_real_and_imag(
                                                          self.kc_pcal_line_freq,
                                                          endstation,
                                                          include_dewhitening)
        self.src_pcal_corr_re, self.src_pcal_corr_im = \
            self._pcal_corr_real_and_imag(self.src_pcal_line_freq,
                                          endstation,
                                          include_dewhitening)
        self.high_pcal_corr_re, self.high_pcal_corr_im = \
            self._pcal_corr_real_and_imag(self.high_pcal_line_freq,
                                          endstation,
                                          include_dewhitening)
        if hasattr(self, 'roaming_pcal_line_freq'):
            self.roaming_pcal_corr_re, self.roaming_pcal_corr_im = \
                self._pcal_corr_real_and_imag(self.roaming_pcal_line_freq,
                                              endstation,
                                              include_dewhitening)
        y_arm_pcal_corr = self.calcs.pcal.compute_pcal_correction(
                                          self.model_freqs,
                                          endstation=endstation,
                                          include_dewhitening=include_dewhitening)
        self.y_arm_pcal_corr = \
            [self.model_freqs, np.real(y_arm_pcal_corr), np.imag(y_arm_pcal_corr)]

    def _compute_epics(self, endstation):
        """ Compute EPICS records using pyDARM and store them as attributes """
        EPICS = self.calcs.compute_epics_records(gds_pcal_endstation=endstation, exact=True)

        # Store their values
        self.ATinvRratio_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_REAL']
        self.ATinvRratio_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_IMAG']
        self.APinvRratio_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_REAL']
        self.APinvRratio_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_IMAG']
        self.AUinvRratio_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_REAL']
        self.AUinvRratio_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_IMAG']
        self.C0_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_REAL']
        self.C0_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_IMAG']
        self.D_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_D_REAL']
        self.D_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_D_IMAG']
        self.AT_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_REAL']
        self.AT_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_IMAG']
        self.AP_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_REAL']
        self.AP_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_IMAG']
        self.AU_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_REAL']
        self.AU_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_IMAG']
        self.C0_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_REAL']
        self.C0_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_IMAG']
        self.D_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_D_REAL']
        self.D_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_D_IMAG']
        self.AT_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_REAL']
        self.AT_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_IMAG']
        self.AP_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_REAL']
        self.AP_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_IMAG']
        self.AU_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_REAL']
        self.AU_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_IMAG']
        self.C0DAT_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_TST_REAL']
        self.C0DAT_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_TST_IMAG']
        self.C0DAP_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_PUM_REAL']
        self.C0DAP_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_PUM_IMAG']
        self.C0DAU_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_UIM_REAL']
        self.C0DAU_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_UIM_IMAG']
        self.C0DAT_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_TST_REAL']
        self.C0DAT_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_TST_IMAG']
        self.C0DAP_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_PUM_REAL']
        self.C0DAP_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_PUM_IMAG']
        self.C0DAU_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_UIM_REAL']
        self.C0DAU_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_UIM_IMAG']
        self.C0AT0_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_A_TST_NL_REAL']
        self.C0AT0_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_A_TST_NL_IMAG']
        self.C0DAT_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_TST_REAL']
        self.C0DAT_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_TST_IMAG']
        self.C0DAP_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_PUM_REAL']
        self.C0DAP_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_PUM_IMAG']
        self.C0DAU_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_UIM_REAL']
        self.C0DAU_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_UIM_IMAG']
        self.C0AP0_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_A_PUM_NL_REAL']
        self.C0AP0_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_A_PUM_NL_IMAG']
        self.C0DAT_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_TST_REAL']
        self.C0DAT_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_TST_IMAG']
        self.C0DAP_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_PUM_REAL']
        self.C0DAP_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_PUM_IMAG']
        self.C0DAU_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_UIM_REAL']
        self.C0DAU_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_UIM_IMAG']
        self.C0AU0_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_A_UIM_NL_REAL']
        self.C0AU0_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_A_UIM_NL_IMAG']
        self.C0DAT_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_TST_REAL']
        self.C0DAT_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_TST_IMAG']
        self.C0DAP_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_PUM_REAL']
        self.C0DAP_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_PUM_IMAG']
        self.C0DAU_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_UIM_REAL']
        self.C0DAU_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_UIM_IMAG']
        self.R_f1_re = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_RESP_REAL']
        self.R_f1_im = EPICS['CAL-CS_TDEP_PCAL_LINE1_REF_RESP_IMAG']
        self.R_f2_re = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_RESP_REAL']
        self.R_f2_im = EPICS['CAL-CS_TDEP_PCAL_LINE2_REF_RESP_IMAG']
        self.RAT0inv_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_RESP_OVER_A_TST_NL_REAL']
        self.RAT0inv_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_RESP_OVER_A_TST_NL_IMAG']
        self.RAP0inv_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_RESP_OVER_A_PUM_NL_REAL']
        self.RAP0inv_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_RESP_OVER_A_PUM_NL_IMAG']
        self.RAU0inv_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_RESP_OVER_A_UIM_NL_REAL']
        self.RAU0inv_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_RESP_OVER_A_UIM_NL_IMAG']
        self.AT0_fT_re = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_A_TST_NL_REAL']
        self.AT0_fT_im = EPICS['CAL-CS_TDEP_SUS_LINE3_REF_A_TST_NL_IMAG']
        self.AP0_fP_re = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_A_PUM_NL_REAL']
        self.AP0_fP_im = EPICS['CAL-CS_TDEP_SUS_LINE2_REF_A_PUM_NL_IMAG']
        self.AU0_fU_re = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_A_UIM_NL_REAL']
        self.AU0_fU_im = EPICS['CAL-CS_TDEP_SUS_LINE1_REF_A_UIM_NL_IMAG']

    def _compute_fd_cal_models(self):
        """
        Compute transfer functions of model values for use to compare with
        FIR filters
        """
        R = self.calcs.compute_response_function(self.model_freqs[1:])
        C = self.calcs.sensing.compute_sensing(self.model_freqs[1:])
        Cinv = 1.0 / C
        A = self.calcs.actuation.compute_actuation(self.model_freqs[1:])
        D = self.calcs.digital.compute_response(self.model_freqs[1:])
        T = self.calcs.actuation.stage_super_actuator(
            self.model_freqs[1:], stage='TST')
        P = self.calcs.actuation.stage_super_actuator(
            self.model_freqs[1:], stage='PUM')
        U = self.calcs.actuation.stage_super_actuator(
            self.model_freqs[1:], stage='UIM')

        # Add in the DC component by hand to avoid RuntimeWarnings
        R = np.insert(R, 0, abs(R[0]))
        Cinv = np.insert(Cinv, 0, abs(C[0]))
        A = np.insert(A, 0, abs(A[0]))
        D = np.insert(D, 0, abs(D[0]))
        T = np.insert(T, 0, abs(T[0]))
        P = np.insert(P, 0, abs(P[0]))
        U = np.insert(U, 0, abs(U[0]))

        # The complex-valued transfer functions computed above are used to
        # compare with the FIR filters. The FIR filters have included a
        # compensation for the model jump delay from OMC to CALCS. In order
        # to account for this, either the FIR filters need to have the
        # advance removed, or include the advance in the model transfer
        # functions calculated above. Here we do the latter.
        model_jump_delay = np.exp(2 * np.pi * 1j * self.model_freqs / 16384.0)
        Cinv *= model_jump_delay
        A *= model_jump_delay
        T *= model_jump_delay
        P *= model_jump_delay
        U *= model_jump_delay

        # Store these as 2D arrays with the frequency vector, real parts, and imaginary parts
        self.response_function = np.asarray((self.model_freqs, np.real(R), np.imag(R)))
        self.invsens_model = np.array((self.model_freqs, np.real(Cinv), np.imag(Cinv)))
        self.act_model = np.array((self.model_freqs, np.real(A), np.imag(A)))
        self.D_model = np.array((self.model_freqs, np.real(D), np.imag(D)))
        self.tst_model = np.array((self.model_freqs, np.real(T), np.imag(T)))
        self.pum_model = np.array((self.model_freqs, np.real(P), np.imag(P)))
        self.uim_model = np.array((self.model_freqs, np.real(U), np.imag(U)))

    def _verify_nonsens_filters(self, nonsens_corr_FIRpars, plots_directory,
                                output_filename, include_advance=True,
                                include_res_corr=False):
        """Plots and sanity checks for NONSENS filters"""
        nonsens_corr_plot_freq = np.arange(
            0,
            nonsens_corr_FIRpars.fNyquist + nonsens_corr_FIRpars.df/8.0,
            nonsens_corr_FIRpars.df/8.0,
        )
        if include_advance:
            nonsens_filter, nonsens_filter_delay = self._compute_linear_phase_fir(
                1/nonsens_corr_FIRpars.dt,
                nonsens_corr_FIRpars.dur / nonsens_corr_FIRpars.dt,
                nonsens_corr_FIRpars.t_advance,
            )
            nonsens_fd_for_plot = freqresp(nonsens_filter, delay_samples=nonsens_filter_delay)
        if include_res_corr:
            res_corr_fd = self._compute_res_corr(nonsens_corr_plot_freq)
            if nonsens_filter is not None:
                nonsens_fd_for_plot *= res_corr_fd
            else:
                nonsens_fd_for_plot = res_corr_fd
        nonsens_corr_FIRpars.check_td_vs_fd(self.nonsens_firfilt, nonsens_fd_for_plot,
                                            filename="%s/nonsens_corr_fd_comparison.png"
                                                     % plots_directory,
                                            plot_title="Nonsens corrections comparison (%s)"
                                                       % output_filename)

    def _generate_nonsens_filter(self, nonsensFIRpars, include_advance=True,
                                 include_res_corr=False):
        """Generate FIR filters for use with NONSENS subtraction.
           These filters can include a delay/advance or additional
           corrections needed for NONSENS subtraction."""
        nonsens_filter = None
        nonsens_filter_delay = nonsensFIRpars.delay_samples
        if include_advance:
            nonsens_filter, nonsens_filter_delay = self._compute_linear_phase_fir(
                1/nonsensFIRpars.dt,
                nonsensFIRpars.dur / nonsensFIRpars.dt,
                nonsensFIRpars.t_advance
            )
            nonsens_model = freqresp(nonsens_filter, samples_per_lobe=1,
                                     delay_samples=nonsens_filter_delay)
        if include_res_corr:
            res_corr_fd = self._compute_res_corr(nonsensFIRpars.freq_array)
            if nonsens_filter is not None:
                nonsens_model *= res_corr_fd
            else:
                nonsens_model = res_corr_fd
            [nonsens_filter, nonsens_model] = nonsensFIRpars.create_fir_filter(nonsens_model)
        self.nonsens_firfilt = nonsens_filter
        self.nonsens_model = nonsens_model
        self.nonsens_firfilt_delay = nonsens_filter_delay

    def _compute_linear_phase_fir(self, sr, filter_samples, t_advance):
        """
        Make a linear phase FIR filter to shift timestamps

        Parameters
        ----------
        sr : int
            sample rate in Hz
        filter_samples : int
            number of taps in the filter
        t_advance : float
            filter advance in units of seconds

        Returns
        -------
        sinc_filter : `float`, array-like
            linear phase sinc filter
        half_filter_shift : int
            half filter length plus number of shift samples
        """
        shift_samples = t_advance * sr

        # Compute filter using odd filter length
        odd_samples = int(filter_samples) - (1 - int(filter_samples) % 2)

        frac_samples = shift_samples % 1

        # Make a filter using a sinc table, slightly shifted relative to the samples
        sinc_arg = np.arange(-int(odd_samples / 2), 1 + int(odd_samples / 2)) + frac_samples
        sinc_filter = np.sinc(sinc_arg)
        # Apply a Blackman window
        sinc_filter *= np.blackman(odd_samples)
        # Normalize the filter
        sinc_filter /= np.sum(sinc_filter)
        # In case filter length is actually even
        if not int(filter_samples) % 2:
            sinc_filter = np.insert(sinc_filter, 0, 0.0)

        half_filter_shift = int(filter_samples / 2) + int(np.floor(shift_samples))

        return sinc_filter, half_filter_shift

    def _save_filters_file(self, output_filename, output_dir,
                           exclude_list=None):
        """ Save FIR filters to file in specified format."""
        root, ext = os.path.splitext(output_filename)
        if ext == '.npz':
            output_filename = output_filename.rstrip(".npz")
            file_format = 'npz'
        elif ext == '.h5':
            output_filename = output_filename.rstrip(".h5")
            file_format = 'hdf5'
        else:
            warnings.warn("Output file must have extension .h5 or .npz.")
        if file_format == 'npz':
            filters = deepcopy(self.__dict__)
            if exclude_list:
                for item in exclude_list:
                    filters.pop(item, None)
            ext = '.npz'
            np.savez(os.path.join(output_dir, f"{root}{ext}"), **filters)
        elif file_format == 'hdf5':
            ext = '.h5'
            hf = h5py.File(os.path.join(output_dir, f"{root}{ext}"), 'w')
            for attribute, value in vars(self).items():
                if attribute in exclude_list:
                    continue
                try:
                    hf.create_dataset(attribute, data=value)
                except TypeError:
                    warnings.warn(f"Could not save {attribute} attribute to "
                                  "filters file. Skipping and moving on...")
            hf.close()
        else:
            raise ValueError("Must provide file format of either 'npz' or 'hdf5'. "
                             f"You provided {file_format}")

    def _save_extra_zeros_poles_ctrl(self):
        """
        Additional zeros necessary to correct the front end output.
        These are optional configs and are dealt with accordingly
        """
        for stage in ['tst', 'pum', 'uim']:
            if hasattr(self.FIR, f'extra_zeros_{stage}'):
                if getattr(self.FIR, f'extra_zeros_{stage}') == '[]':
                    setattr(self, f'extra_zeros_{stage}', [])
                else:
                    setattr(self, f'extra_zeros_{stage}',
                            float(getattr(self.FIR,
                                  f'extra_zeros_{stage}').strip('[]').split(',')))
            else:
                setattr(self, f'extra_zeros_{stage}', [])
            if hasattr(self.FIR, f'extra_delay_{stage}'):
                setattr(self, f'extra_delay_{stage}', getattr(
                    self.FIR, f'extra_delay_{stage}'))
            else:
                setattr(self, f'extra_delay_{stage}', 0)

    def _compute_ctrl_corr(self, freqs, stage):
        """ Compute FIR filter for control branch correction."""
        if freqs[0] == 0.0:
            # Don't try to calculate the response at zero frequency
            ctrl_corr_fd = self.calcs.gds_actuation_correction(freqs[1:], stage=stage)
            # Add in the DC component by hand
            ctrl_corr_fd = np.insert(ctrl_corr_fd, 0, 0)
        else:
            ctrl_corr_fd = self.calcs.gds_actuation_correction(freqs, stage=stage)
        extra_zeros = getattr(self, f'extra_zeros_{stage.lower()}')
        extra_delay = getattr(self, f'extra_delay_{stage.lower()}')
        for i in range(len(extra_zeros)):
            ctrl_corr_fd *= (1 + 1j * freqs / extra_zeros[i])
        ctrl_corr_fd *= np.exp(-2 * np.pi * 1j * freqs * float(extra_delay))

        if not hasattr(self.FIR, "response_corr_cutoff"):
            self.FIR.response_corr_cutoff = 2 * self.FIR.res_corr_fnyq
            if hasattr(self.FIR, "exclude_response_corr"):
                if self.FIR.exclude_response_corr:
                    self.FIR.response_corr_cutoff = 0.0
        if self.FIR.response_corr_cutoff > self.FIR.ctrl_corr_fnyq:
            # Since we downsample the actuation, we'll use the inverse sensing filter
            # to model the entire response above the Nyquist rate of the actuation path.
            # We will therefore smoothly roll off the actuation filter as it
            # approaches the Nyquist rate.
            df = freqs[1] - freqs[0]
            full_hann = np.hanning(round(self.FIR.ctrl_corr_fnyq / df / 8))
            half_hann = full_hann[(len(full_hann) // 2 + 1):]
            ctrl_corr_fd[len(ctrl_corr_fd) - len(half_hann):] *= half_hann
        return ctrl_corr_fd

    def _generate_ctrl_corr_filters(self, ctrl_corr_FIRpars, ctrl_highpass_FIRpars):
        """ Generate filters for control chain corrections."""
        # Process extra zeros and poles if needed
        self._save_extra_zeros_poles_ctrl()

        # Generate control chain correction models
        TST_corr_fd = self._compute_ctrl_corr(ctrl_corr_FIRpars.freq_array, 'TST')
        PUM_corr_fd = self._compute_ctrl_corr(ctrl_corr_FIRpars.freq_array, 'PUM')
        UIM_corr_fd = self._compute_ctrl_corr(ctrl_corr_FIRpars.freq_array, 'UIM')

        # Generate control chain FIR filters
        if ctrl_highpass_FIRpars is not None:
            [self.ctrl_highpass_filter, self.ctrl_highpass_model] = \
                ctrl_highpass_FIRpars.create_fir_filter(
                            np.ones(1 +
                                    int(round(ctrl_highpass_FIRpars.fNyquist /
                                        ctrl_highpass_FIRpars.df))))
        else:
            [self.ctrl_highpass_filter, self.ctrl_highpass_model] = [[], []]

        [self.TST_corr_filter, self.TST_corr_filt_model] = ctrl_corr_FIRpars.create_fir_filter(
                                                                             TST_corr_fd)
        [self.PUM_corr_filter, self.PUM_corr_filt_model] = ctrl_corr_FIRpars.create_fir_filter(
                                                                             PUM_corr_fd)
        [self.UIM_corr_filter, self.UIM_corr_filt_model] = ctrl_corr_FIRpars.create_fir_filter(
                                                                             UIM_corr_fd)

    def _generate_res_corr_noccpole(self, freqs, res_corr_fd):
        """
        Generate an inverse sensing residual correction filter
        that does not include the coupled cavity pole.
        Divide out the response of the two-tap filter that would be used to apply the cavity pole.
        """
        res_corr_noccpole_fd = \
            res_corr_fd / two_tap_zero_filter_response([self.fcc], 16384, freqs)
        return res_corr_noccpole_fd

    def _generate_res_corr_nopole(self, freqs, res_corr_fd, res_corr_noccpole_fd):
        """ Generate residual correction filter without any poles."""
        if np.real(self.fs) != 0 and self.srcQ != 0:
            srQ = np.sqrt(1.0 / self.srcQ / self.srcQ + 4.0)
            fsrQ1 = (self.fs / 2.0) * (1.0 / self.srcQ + srQ)
            fsrQ2 = (self.fs / 2.0) * (1.0 / self.srcQ - srQ)
            res_corr_nopole_fd = \
                res_corr_fd / two_tap_zero_filter_response([self.fcc, fsrQ1, fsrQ2],
                                                           16384, freqs)
            # fs^2 is a gain factor as well
            res_corr_nopole_fd /= self.fs_squared
        else:
            res_corr_nopole_fd = np.copy(res_corr_noccpole_fd)

        # Multiply by f^2
        res_corr_nopole_fd *= freqs * freqs
        return res_corr_nopole_fd

    def _compute_res_corr(self, freqs):
        """ Compute sensing correction for GDS pipeline."""
        if not hasattr(self.FIR, "response_corr_cutoff"):
            self.FIR.response_corr_cutoff = 2 * self.FIR.res_corr_fnyq
            if hasattr(self.FIR, "exclude_response_corr"):
                if self.FIR.exclude_response_corr:
                    self.FIR.response_corr_cutoff = 0.0
        if freqs[0] == 0.0:
            # Don't try to calculate response at zero frequency
            res_corr_fd = self.calcs.gds_sensing_correction(freqs[1:])
            if self.FIR.response_corr_cutoff > self.FIR.ctrl_corr_fnyq:
                C = self.calcs.sensing.compute_sensing(freqs[1:])
                R = self.calcs.compute_response_function(freqs[1:])
            # Add in DC compoment by hand
            res_corr_fd = np.insert(res_corr_fd, 0, 0)
            if self.FIR.response_corr_cutoff > self.FIR.ctrl_corr_fnyq:
                C = np.insert(C, 0, 0)
                R = np.insert(R, 0, 0)
        else:
            res_corr_fd = self.calcs.gds_sensing_correction(freqs)
            if self.FIR.response_corr_cutoff > self.FIR.ctrl_corr_fnyq:
                C = self.calcs.sensing.compute_sensing(freqs)
                R = self.calcs.compute_response_function(freqs)

        # Since we downsample the actuation, compensate for the small loss of accuracy
        # by smoothly changing C_corr to 1/R_corr above the actuation path's Nyquist rate
        if self.FIR.response_corr_cutoff > self.FIR.ctrl_corr_fnyq:
            sensing_corr_fd = 1.0 / res_corr_fd
            invsens_calcs = sensing_corr_fd / C
            response_inv_corr = invsens_calcs / R
            Cwindow = np.ones(len(sensing_corr_fd))
            df = freqs[1] - freqs[0]
            full_hann = np.hanning(round(self.FIR.ctrl_corr_fnyq / df / 8))
            half_hann = full_hann[(len(full_hann) // 2 + 1):]
            indexNy = round(self.FIR.ctrl_corr_fnyq / df)
            Cwindow[indexNy - len(half_hann):indexNy] = half_hann
            if self.FIR.response_corr_cutoff < self.FIR.res_corr_fnyq:
                index_end = round(self.FIR.response_corr_cutoff / df)
                index_start = max(index_end - len(half_hann), indexNy)
                Cwindow[index_start:index_end] *= half_hann[::-1][index_start - index_end:]
                Cwindow[indexNy:index_start] = 0
            else:
                Cwindow[indexNy:] = 0
            Rwindow = np.ones(len(sensing_corr_fd)) - Cwindow
            sensing_corr_fd = Cwindow * sensing_corr_fd + Rwindow * response_inv_corr
            res_corr_fd = 1.0 / sensing_corr_fd

        # Set DC component to 0 by hand
        res_corr_fd[0] = 0
        return res_corr_fd

    def _generate_res_corr_filters(self, res_corr_FIRpars, res_corr_highpass_FIRpars):
        """ Generate GDS correction filters for residual chain."""
        # Generate residual chain highpass filter
        res_corr_highpass_fnyq_df = \
            np.ones(1+int(round(res_corr_highpass_FIRpars.fNyquist/res_corr_highpass_FIRpars.df)))
        if res_corr_highpass_FIRpars is not None:
            [self.res_highpass, self.res_highpass_model] = \
                res_corr_highpass_FIRpars.create_fir_filter(res_corr_highpass_fnyq_df)
        else:
            [self.res_highpass, self.res_highpass_model] = [[], []]

        # Generate residual chain correction filter
        res_corr_fd = self._compute_res_corr(res_corr_FIRpars.freq_array)
        [self.res_corr_filter, self.res_corr_filt_model] = res_corr_FIRpars.create_fir_filter(
                                                                            res_corr_fd)

        # Generate residual chain correction filter with no cc pole
        res_corr_noccpole_fd = self._generate_res_corr_noccpole(res_corr_FIRpars.freq_array,
                                                                res_corr_fd)
        [self.res_corr_noccpole_filter, self.res_corr_noccpole_model] = \
            res_corr_FIRpars.create_fir_filter(res_corr_noccpole_fd)

        # Generate an residual chain correction filter that
        # does not include the coupled cavity pole or SRC detuning.
        res_corr_nopole_fd = self._generate_res_corr_nopole(res_corr_FIRpars.freq_array,
                                                            res_corr_fd,
                                                            res_corr_noccpole_fd)
        [res_corr_nopole_td, model] = res_corr_FIRpars.create_fir_filter(res_corr_nopole_fd)
        res_corr_nopole_fd = correctFIRfilter([res_corr_FIRpars, res_corr_highpass_FIRpars],
                                              [res_corr_nopole_td, self.res_highpass],
                                              res_corr_nopole_fd, [5, 9, 100, 150])
        [self.res_corr_nopole_filter, self.res_corr_nopole_model] = \
            res_corr_FIRpars.create_fir_filter(res_corr_nopole_fd)

    def _verify_res_corr_filters(self, res_corr_FIRpars, res_corr_highpass_FIRpars,
                                 plots_directory, output_filename):
        """
        Sample the model at 8 times the frequency resolution of the filter,
        and test the filter at that frequency resolution as well.
        (computeFIRfilters.check_td_vs_fd does that by default.)
        """

        # Generate the res correction for the plot
        res_corr_plot_freq = np.arange(0, res_corr_FIRpars.fNyquist + res_corr_FIRpars.df / 8.0,
                                       res_corr_FIRpars.df / 8.0)
        res_corr_fd_for_plot = self._compute_res_corr(res_corr_plot_freq)

        # Generate highpass for the plot
        if res_corr_highpass_FIRpars is not None:
            res_corr_highpass_fd_for_plot = \
                np.ones(1+int(round(res_corr_highpass_FIRpars.fNyquist /
                                    res_corr_highpass_FIRpars.df/8.0)))

        # Generate a res correction without cavity pole for the plot
        res_corr_noccpole_fd_for_plot = self._generate_res_corr_noccpole(res_corr_plot_freq,
                                                                         res_corr_fd_for_plot)

        # Generate a model without SRC params or cavity pole for the plot
        res_corr_nopole_fd_for_plot = self._generate_res_corr_nopole(res_corr_plot_freq,
                                                                     res_corr_fd_for_plot,
                                                                     res_corr_noccpole_fd_for_plot)

        res_corr_FIRpars.check_td_vs_fd(self.res_corr_filter, res_corr_fd_for_plot,
                                        filename=os.path.join(plots_directory,
                                                              "rescorr_fd_comparison.png"),
                                        plot_title=f"Res Corr comparison ({output_filename})")

        if res_corr_highpass_FIRpars is not None:
            res_corr_highpass_FIRpars.check_td_vs_fd(
                self.res_highpass,
                res_corr_highpass_fd_for_plot,
                filename=os.path.join(plots_directory, "rescorr_highpass_fd_comparison.png"),
                plot_title=f"Residual corrections highpass comparison ({output_filename})")

        res_corr_FIRpars.check_td_vs_fd(self.res_corr_noccpole_filter,
                                        res_corr_noccpole_fd_for_plot,
                                        filename=os.path.join(plots_directory,
                                                              "rescorr_noccpole_fd_comparison.png"),
                                        plot_title=f"Res Corr No CC Pole comparison \
                                                    ({output_filename})")
        res_corr_FIRpars.check_td_vs_fd(self.res_corr_nopole_filter, res_corr_nopole_fd_for_plot,
                                        filename=os.path.join(plots_directory,
                                                              "rescorr_nopole_fd_comparison.png"),
                                        plot_title=f"Res Corr No Pole \
                                                     comparison ({output_filename})",
                                        ymax_increase=10000000)

    def _verify_ctrl_corr_filters(self, ctrl_corr_FIRpars, ctrl_corr_highpass_FIRpars,
                                  plots_directory, output_filename):
        """ Check the control correction filters with sanity checks."""
        # Generate ctrl correction model at 8 times the frequency resolution of the filter
        ctrl_corr_plot_freq = np.arange(0, ctrl_corr_FIRpars.fNyquist + ctrl_corr_FIRpars.df / 8.0,
                                        ctrl_corr_FIRpars.df / 8.0)
        TST_corr_for_plot = self._compute_ctrl_corr(ctrl_corr_plot_freq, 'TST')
        PUM_corr_for_plot = self._compute_ctrl_corr(ctrl_corr_plot_freq, 'PUM')
        UIM_corr_for_plot = self._compute_ctrl_corr(ctrl_corr_plot_freq, 'UIM')

        if ctrl_corr_highpass_FIRpars is not None:
            ctrl_corr_highpass_fd_for_plot = np.ones(1 +
                                                     int(round(ctrl_corr_highpass_FIRpars.fNyquist /
                                                               ctrl_corr_highpass_FIRpars.df/8.0)))
        ctrl_corr_FIRpars.check_td_vs_fd(self.TST_corr_filter, TST_corr_for_plot,
                                         filename=os.path.join(plots_directory,
                                                               "TST_corr_fd_comparison.png"),
                                         plot_title=f"TST corrections comparison \
                                                      ({output_filename})")
        ctrl_corr_FIRpars.check_td_vs_fd(self.PUM_corr_filter, PUM_corr_for_plot,
                                         filename=os.path.join(plots_directory,
                                                               "PUM_corr_fd_comparison.png"),
                                         plot_title=f"PUM corrections comparison \
                                                     ({output_filename})")
        ctrl_corr_FIRpars.check_td_vs_fd(self.UIM_corr_filter, UIM_corr_for_plot,
                                         filename=os.path.join(plots_directory,
                                                               "UIM_corr_fd_comparison.png"),
                                         plot_title=f"UIM corrections comparison \
                                                     ({output_filename})")
        if ctrl_corr_highpass_FIRpars is not None:
            ctrl_corr_highpass_FIRpars.check_td_vs_fd(
                self.ctrl_corr_highpass_filter,
                ctrl_corr_highpass_fd_for_plot,
                filename=os.path.join(plots_directory, "ctrl_corr_highpass_fd_comparison.png"),
                plot_title=f"CTRL correction highpass comparison ({output_filename})")

    def GDS(self, output_filename='GDS.npz',
            output_dir='.', plots_directory=None):
        """
        GDS FIR filter generation

        Parameters
        ----------
        output_filename : str
            Output filename
        output_dir : str
            Directory to which to save FIR filters file
        plots_directory : str
            Directory to which to save diagnostic plots.

        Returns
        -------
        output_filename, diagnostic plots of filters

        """

        # Compute ctrl chain correction FIR parameters
        ctrl_corr_FIRpars = FIRfilter(fNyq=self.FIR.ctrl_corr_fnyq,
                                      desired_dur=self.FIR.ctrl_corr_duration,
                                      highpass_fcut=self.FIR.ctrl_corr_highpass_fcut,
                                      window_type=self.FIR.ctrl_corr_window_type,
                                      freq_res=self.FIR.ctrl_corr_freq_res)

        # If we want to generate a separate highpass filter, do so
        if self.FIR.ctrl_corr_highpass_duration != "" and \
           self.FIR.ctrl_corr_highpass_duration != 0.0:
            ctrl_corr_highpass_FIRpars = FIRfilter(fNyq=self.FIR.ctrl_corr_fnyq,
                                                   desired_dur=self.FIR.ctrl_corr_highpass_duration,
                                                   highpass_fcut=self.FIR.ctrl_corr_highpass_fcut,
                                                   window_type=self.FIR.ctrl_corr_window_type,
                                                   freq_res=self.FIR.ctrl_corr_highpass_freq_res)
        else:
            ctrl_corr_highpass_FIRpars = None

        # Generate the ctrl chain correction FIR filters
        self._generate_ctrl_corr_filters(ctrl_corr_FIRpars, ctrl_corr_highpass_FIRpars)

        # Compute res chain correction FIR parameters
        res_corr_FIRpars = FIRfilter(fNyq=self.FIR.res_corr_fnyq,
                                     desired_dur=self.FIR.res_corr_duration,
                                     lowpass_fcut=self.FIR.res_corr_lowpass_fcut,
                                     highpass_fcut=self.FIR.res_corr_highpass_fcut,
                                     window_type=self.FIR.res_corr_window_type,
                                     freq_res=self.FIR.res_corr_freq_res)

        # If we want to generate a separate highpass filter, do so
        if self.FIR.res_corr_highpass_duration != "" and self.FIR.res_corr_highpass_duration != 0.0:
            res_corr_highpass_FIRpars = FIRfilter(fNyq=self.FIR.res_corr_highpass_fnyq,
                                                  desired_dur=self.FIR.res_corr_highpass_duration,
                                                  highpass_fcut=self.FIR.res_corr_highpass_fcut,
                                                  window_type=self.FIR.res_corr_window_type,
                                                  freq_res=self.FIR.res_corr_highpass_freq_res)
        else:
            res_corr_highpass_FIRpars = None

        # Generate res chain FIR filters
        self._generate_res_corr_filters(res_corr_FIRpars, res_corr_highpass_FIRpars)

        # Compute FIR filter parameters for nonsens subtraction filter
        nonsens_corr_FIRpars = FIRfilter(fNyq=self.FIR.nonsens_corr_fnyq,
                                         desired_dur=self.FIR.nonsens_corr_duration,
                                         highpass_fcut=self.FIR.nonsens_corr_highpass_fcut,
                                         lowpass_fcut=self.FIR.nonsens_corr_lowpass_fcut,
                                         window_type=self.FIR.nonsens_corr_window_type,
                                         freq_res=self.FIR.nonsens_corr_freq_res)
        if self.FIR.include_nonsens_advance:
            nonsens_corr_FIRpars.t_advance = self.FIR.nonsens_corr_advance

        # Generate nonsens FIR filter correction
        self._generate_nonsens_filter(nonsens_corr_FIRpars,
                                      include_advance=self.FIR.include_nonsens_advance,
                                      include_res_corr=self.FIR.include_nonsens_res_corr)

        if plots_directory is not None:
            # Verify  FIR filters
            os.makedirs(plots_directory, exist_ok=True)
            self._verify_res_corr_filters(res_corr_FIRpars,
                                          res_corr_highpass_FIRpars,
                                          plots_directory,
                                          output_filename)
            self._verify_ctrl_corr_filters(ctrl_corr_FIRpars,
                                           ctrl_corr_highpass_FIRpars,
                                           plots_directory,
                                           output_filename)
            self._verify_nonsens_filters(nonsens_corr_FIRpars,
                                         plots_directory,
                                         output_filename,
                                         include_advance=self.FIR.include_nonsens_advance,
                                         include_res_corr=self.FIR.include_nonsens_res_corr)
            self.figs.extend(res_corr_FIRpars.figs)
            self.figs.extend(nonsens_corr_FIRpars.figs)
            if res_corr_highpass_FIRpars is not None:
                self.figs.extend(res_corr_highpass_FIRpars.figs)
            self.figs.extend(ctrl_corr_FIRpars.figs)
            if ctrl_corr_highpass_FIRpars is not None:
                self.figs.extend(ctrl_corr_highpass_FIRpars.figs)

        # Save last items as attributes so they are saved to filters file
        self.res_corr_delay = res_corr_FIRpars.delay_samples
        if res_corr_highpass_FIRpars is not None:
            self.res_highpass_delay = res_corr_highpass_FIRpars.delay_samples
            self.res_highpass_sr = res_corr_highpass_FIRpars.fNyquist * 2
        else:
            self.res_highpass_delay = 0
            self.res_highpass_sr = 0
        self.ctrl_corr_delay = ctrl_corr_FIRpars.delay_samples
        if ctrl_corr_highpass_FIRpars is not None:
            self.ctrl_highpass_delay = ctrl_corr_highpass_FIRpars.delay_samples
        else:
            self.ctrl_highpass_delay = 0
        self.ctrl_corr_sr = ctrl_corr_FIRpars.fNyquist * 2
        self.invsens_window_type = res_corr_FIRpars.window_type
        self.invsens_freq_res = res_corr_FIRpars.freq_res
        self.act_window_type = ctrl_corr_FIRpars.window_type
        self.act_freq_res = ctrl_corr_FIRpars.freq_res
        # FIXME: This should be removed when gstlal_compute_strain doesn't require it
        self.ctrl_corr_filter = self.TST_corr_filter

        # Save the filters file
        self._save_filters_file(output_filename, output_dir, exclude_list=self.exclude_from_filters)

    def _compute_act(self, freqs, stage):
        """ Compute actuation in frequency domain."""
        if freqs[0] == 0.0:
            # Don't try to calculate the response at zero frequency
            act_fd = self.calcs.actuation.stage_super_actuator(
                freqs[1:], stage=stage)
            # Add in the DC component by hand to avoid RuntimeWarnings
            act_fd = np.insert(act_fd, 0, 0)
        else:
            act_fd = self.calcs.actuation.stage_super_actuator(freqs, stage=stage)

        # Account for model jump delay
        model_jump_delay = np.exp(2 * np.pi * 1j * freqs / 16384.0)
        act_fd *= model_jump_delay

        if not hasattr(self.FIR, "response_corr_cutoff"):
            self.FIR.response_corr_cutoff = 2 * self.FIR.invsens_fnyq
            if hasattr(self.FIR, "exclude_response_corr"):
                if self.FIR.exclude_response_corr:
                    self.FIR.response_corr_cutoff = 0.0
        if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
            # Since we downsample the actuation, we'll use the inverse sensing filter to
            # model the entire response above the Nyquist rate of the actuation path.
            # We will therefore smoothly roll off the actuation filter
            # as it approaches the Nyquist rate.
            df = freqs[1] - freqs[0]
            full_hann = np.hanning(round(self.FIR.act_fnyq / df / 8))
            half_hann = full_hann[(len(full_hann) // 2 + 1):]
            act_fd[len(act_fd) - len(half_hann):] *= half_hann
        return act_fd

    def _generate_act_filters(self, A_FIRpars, A_highpass_FIRpars):
        """ Generate all filters for the actuation chain."""
        # Create actuation model
        tst_fd = self._compute_act(A_FIRpars.freq_array, 'TST')
        pum_fd = self._compute_act(A_FIRpars.freq_array, 'PUM')
        uim_fd = self._compute_act(A_FIRpars.freq_array, 'UIM')

        # Generate FIR filter from frequency-domain model
        if A_highpass_FIRpars is not None:
            [self.actuation_highpass, self.act_highpass_model] = \
                A_highpass_FIRpars.create_fir_filter(
                            np.ones(1 + int(round(A_FIRpars.fNyquist/A_FIRpars.df))))
        else:
            [self.actuation_highpass, self.act_highpass_model] = [[], []]
        [self.actuation_tst, self.tstfilt_model] = self._create_act_FIR_filter(
                                                       tst_fd,
                                                       self.actuation_highpass,
                                                       A_FIRpars,
                                                       A_highpass_FIRpars)
        [self.actuation_pum, self.pumfilt_model] = self._create_act_FIR_filter(
                                                       pum_fd,
                                                       self.actuation_highpass,
                                                       A_FIRpars,
                                                       A_highpass_FIRpars)
        [self.actuation_uim, self.uimfilt_model] = self._create_act_FIR_filter(
                                                       uim_fd,
                                                       self.actuation_highpass,
                                                       A_FIRpars,
                                                       A_highpass_FIRpars)

    def _create_act_FIR_filter(self, act_fd, act_highpass_td, act_FIRpars, act_highpass_FIRpars):
        """ Create a specific FIR filters for actuation chain."""
        [act_td, actfilt_model] = act_FIRpars.create_fir_filter(act_fd)
        if act_highpass_FIRpars is not None:
            act_fd = correctFIRfilter([act_FIRpars, act_highpass_FIRpars],
                                      [act_td, act_highpass_td], act_fd,
                                      [5, 10, 100, 150])
        else:
            act_fd = correctFIRfilter([act_FIRpars],
                                      [act_td],
                                      act_fd,
                                      [5, 10, 100, 150])
        [act_td, actfilt_model] = act_FIRpars.create_fir_filter(act_fd)
        return act_td, actfilt_model

    def _compute_inverse_sensing(self, freqs):
        """ Compute inverse sensing in the frequency domain."""
        if not hasattr(self.FIR, "response_corr_cutoff"):
            self.FIR.response_corr_cutoff = 2 * self.FIR.invsens_fnyq
            if hasattr(self.FIR, "exclude_response_corr"):
                if self.FIR.exclude_response_corr:
                    self.FIR.response_corr_cutoff = 0.0
        if freqs[0] == 0.0:
            # Don't try to calculate the response at zero frequency
            C = self.calcs.sensing.compute_sensing(freqs[1:])
            if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
                R = self.calcs.compute_response_function(freqs[1:])
            Cinv = 1.0 / C
            Cinv = np.insert(Cinv, 0, 0)
            if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
                R = np.insert(R, 0, 0)
        else:
            C = self.calcs.sensing.compute_sensing(freqs)
            if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
                R = self.calcs.compute_response_function(freqs)
        # Account for model jump delay
        model_jump_delay = np.exp(2 * np.pi * 1j * freqs / 16384.0)
        Cinv *= model_jump_delay
        if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
            R *= model_jump_delay

        # Since we downsample the actuation, compensate for the small loss of
        # accuracy by smoothly changing C_corr to 1/R_corr above
        # the actuation path's Nyquist rate
        if self.FIR.response_corr_cutoff > self.FIR.act_fnyq:
            Cwindow = np.ones(len(Cinv))
            df = freqs[1]-freqs[0]
            full_hann = np.hanning(round(self.FIR.act_fnyq / df / 8))
            half_hann = full_hann[(len(full_hann) // 2 + 1):]
            indexNy = round(self.FIR.act_fnyq / df)
            Cwindow[indexNy - len(half_hann):indexNy] = half_hann
            if self.FIR.response_corr_cutoff < self.FIR.invsens_fnyq:
                index_end = round(self.FIR.response_corr_cutoff / df)
                index_start = max(index_end - len(half_hann), indexNy)
                Cwindow[index_start:index_end] *= half_hann[::-1][index_start - index_end:]
                Cwindow[indexNy:index_start] = 0
            else:
                Cwindow[indexNy:] = 0
            Rwindow = np.ones(len(Cinv)) - Cwindow
            Cinv = Cwindow * Cinv + Rwindow * R

        # Make sure the DC component is zero
        Cinv[0] = 0
        return Cinv

    def _generate_invsens_noccpole(self, freqs, invsens):
        """ Generate inverse sensing without coupled cavity pole."""
        invsens_noccpole = invsens / two_tap_zero_filter_response([self.fcc], 16384, freqs)
        return invsens_noccpole

    def _generate_invsens_nopole(self, freqs, invsens, invsens_noccpole):
        """ Generate inverse sensing without any poles."""
        freqA = (self.fs / 2.0) * (1.0 / self.srcQ + np.sqrt(1.0 / self.srcQ / self.srcQ + 4.0))
        freqB = (self.fs / 2.0) * (1.0 / self.srcQ - np.sqrt(1.0 / self.srcQ / self.srcQ + 4.0))
        if np.real(self.fs) != 0 and self.srcQ != 0:
            invsens_nopole = invsens / two_tap_zero_filter_response([self.fcc, freqA, freqB],
                                                                    16384, freqs)
        else:
            invsens_nopole = np.copy(invsens_noccpole)
        return invsens_nopole

    def _generate_invsens_filters(self, Cinv_FIRpars, Cinv_highpass_FIRpars):
        """ Generate all filters for inverse sensing chain."""
        # Compute frequency domain model for inverse sensing
        Cinv = self._compute_inverse_sensing(Cinv_FIRpars.freq_array)

        # Generate FIR filter from frequency-domain model
        if Cinv_highpass_FIRpars is not None:
            [self.inv_sensing_highpass, self.invsens_highpass_model] = \
                Cinv_highpass_FIRpars.create_fir_filter(
                    np.ones(1 + int(round(
                        Cinv_highpass_FIRpars.fNyquist/Cinv_highpass_FIRpars.df))))
        else:
            [self.inv_sensing_highpass, self.invsens_highpass_model] = [[], []]

        [self.inv_sensing, self.invsensfilt_model] = Cinv_FIRpars.create_fir_filter(Cinv)

        # Generate an inverse sensing FIR filter
        # that does not include the coupled cavity pole.
        # Divide out the response of the two-tap filter
        # that would be used to apply the cavity pole.
        Cinv_noccpole = self._generate_invsens_noccpole(Cinv_FIRpars.freq_array, Cinv)
        [self.inv_sensing_noccpole, self.inv_sensing_noccpole_model] = \
            Cinv_FIRpars.create_fir_filter(Cinv_noccpole)

        # Generate an inverse sensing FIR filter that
        # does not include the coupled cavity pole or SRC detuning.
        Cinv_nopole = self._generate_invsens_nopole(Cinv_FIRpars.freq_array, Cinv, Cinv_noccpole)
        [self.inv_sensing_nopole, self.inv_sensing_nopole_model] = Cinv_FIRpars.create_fir_filter(
                                                                       Cinv_nopole)

    def _verify_act_filters(self, A_FIRpars, A_highpass_FIRpars, plots_directory, output_filename):
        """ Sanity checks on actuation filters."""
        # Sample the model at 8 times the frequency resolution of the filter,
        # and test the filter at that frequency resolution as well.
        # (computeFIRfilters.check_td_vs_fd does that by default.)

        # Generate the actuation correction for the plot
        A_freq_plot = np.arange(0, A_FIRpars.fNyquist + A_FIRpars.df / 8.0,
                                A_FIRpars.df / 8.0)

        if A_highpass_FIRpars is not None:
            A_highpass_fd_for_plot = np.ones(1 +
                                             int(round(A_highpass_FIRpars.fNyquist /
                                                 A_highpass_FIRpars.df / 8.0)))

        tst_fd_for_plot = self._compute_act(A_freq_plot, 'TST')
        pum_fd_for_plot = self._compute_act(A_freq_plot, 'PUM')
        uim_fd_for_plot = self._compute_act(A_freq_plot, 'UIM')

        A_FIRpars.check_td_vs_fd(self.actuation_tst, tst_fd_for_plot,
                                 filename="%s/tst_actuation_fd_comparison.png"
                                          % plots_directory,
                                 plot_title="TST actuation comparison (%s)"
                                            % output_filename)
        A_FIRpars.check_td_vs_fd(self.actuation_pum, pum_fd_for_plot,
                                 filename="%s/pum_actuation_fd_comparison.png"
                                          % plots_directory,
                                 plot_title="PUM actuation comparison (%s)"
                                            % output_filename)
        A_FIRpars.check_td_vs_fd(self.actuation_uim, uim_fd_for_plot,
                                 filename="%s/uim_actuation_fd_comparison.png"
                                          % plots_directory,
                                 plot_title="UIM actuation comparison (%s)"
                                            % output_filename)
        if A_highpass_FIRpars is not None:
            A_highpass_FIRpars.check_td_vs_fd(self.actuation_highpass,
                                              A_highpass_fd_for_plot,
                                              filename="%s/A_highpass_fd_comparison.png" %
                                              plots_directory,
                                              plot_title="Actuation highpass comparison (%s)" %
                                              output_filename)

    def _verify_invsens_filters(self, Cinv_FIRpars, Cinv_highpass_FIRpars,
                                plots_directory, output_filename):
        """ Sanity checks on inverse sensing filters."""
        # Sample the model at 8 times the frequency resolution of the filter,
        # and test the filter at that frequency resolution as well.
        # (computeFIRfilters.check_td_vs_fd does that by default.)

        # Generate the inverse sensing filter for the plot
        CinvPlot_freq = np.arange(0, Cinv_FIRpars.fNyquist + Cinv_FIRpars.df / 8.0,
                                  Cinv_FIRpars.df / 8.0)
        invsens_fd_for_plot = self._compute_inverse_sensing(CinvPlot_freq)

        invsens_noccpole_fd_for_plot = self._generate_invsens_noccpole(CinvPlot_freq,
                                                                       invsens_fd_for_plot)
        invsens_nopole_fd_for_plot = self._generate_invsens_nopole(CinvPlot_freq,
                                                                   invsens_fd_for_plot,
                                                                   invsens_noccpole_fd_for_plot)

        if Cinv_highpass_FIRpars is not None:
            invsens_highpass_fd_for_plot = np.ones(1 + int(round(Cinv_FIRpars.fNyquist /
                                                                 Cinv_FIRpars.df / 8.0)))

        Cinv_FIRpars.check_td_vs_fd(self.inv_sensing, invsens_fd_for_plot,
                                    filename="%s/invsens_fd_comparison.png"
                                             % plots_directory,
                                    plot_title="Inverse sensing comparison (%s)"
                                               % output_filename)
        Cinv_FIRpars.check_td_vs_fd(self.inv_sensing_noccpole, invsens_noccpole_fd_for_plot,
                                    filename="%s/invsens_noccpole_fd_comparison.png"
                                             % plots_directory,
                                    plot_title="1/C No CC Pole comparison (%s)"
                                               % output_filename)
        Cinv_FIRpars.check_td_vs_fd(self.inv_sensing_nopole, invsens_nopole_fd_for_plot,
                                    filename="%s/invsens_nopole_fd_comparison.png"
                                             % plots_directory,
                                    plot_title="1/C No Pole comparison (%s)"
                                               % output_filename)
        if Cinv_highpass_FIRpars is not None:
            Cinv_highpass_FIRpars.check_td_vs_fd(self.inv_sensing_highpass,
                                                 invsens_highpass_fd_for_plot,
                                                 filename="%s/invsens_highpass_fd_comparison.png"
                                                 % plots_directory,
                                                 plot_title="1/C highpass comparison (%s)"
                                                            % output_filename)

    def DCS(self, output_filename='DCS.npz',
            output_dir='.', plots_directory=None):
        """
        DCS FIR filter generation

        Parameters
        ----------
        output_filename : str
            Output filename
        output_directory : str
            Directory to which to save FIR filters file
        plots_directory : str
            Directory to which to save diagnostic plots.

        Returns
        -------
        output_filename, diagnostic plots of filters

        """
        # Compute FIR filter parameters for actuation and inverse sensing
        A_FIRpars = FIRfilter(fNyq=self.FIR.act_fnyq,
                              desired_dur=self.FIR.act_duration,
                              highpass_fcut=self.FIR.act_highpass_fcut,
                              window_type=self.FIR.act_window_type,
                              freq_res=self.FIR.act_freq_res)
        if self.FIR.act_highpass_duration != "" and self.FIR.act_highpass_duration != 0.0:
            A_highpass_FIRpars = FIRfilter(fNyq=self.FIR.act_fnyq,
                                           desired_dur=self.FIR.act_highpass_duration,
                                           highpass_fcut=self.FIR.act_highpass_fcut,
                                           window_type=self.FIR.act_window_type,
                                           freq_res=self.FIR.act_highpass_freq_res)
        else:
            A_highpass_FIRpars = None
        Cinv_FIRpars = FIRfilter(fNyq=self.FIR.invsens_fnyq,
                                 desired_dur=self.FIR.invsens_duration,
                                 lowpass_fcut=self.FIR.invsens_lowpass_fcut,
                                 highpass_fcut=self.FIR.invsens_highpass_fcut,
                                 window_type=self.FIR.invsens_window_type,
                                 freq_res=self.FIR.invsens_freq_res)
        if self.FIR.invsens_highpass_duration != "" and self.FIR.invsens_highpass_duration != 0.0:
            Cinv_highpass_FIRpars = FIRfilter(fNyq=self.FIR.invsens_highpass_fnyq,
                                              desired_dur=self.FIR.invsens_highpass_duration,
                                              highpass_fcut=self.FIR.invsens_highpass_fcut,
                                              window_type=self.FIR.invsens_window_type,
                                              freq_res=self.FIR.invsens_highpass_freq_res)
        else:
            Cinv_highpass_FIRpars = None

        # Generate actuation FIR filters
        self._generate_act_filters(A_FIRpars, A_highpass_FIRpars)

        # Generate inverse sensing FIR filters
        self._generate_invsens_filters(Cinv_FIRpars, Cinv_highpass_FIRpars)

        if Cinv_highpass_FIRpars is not None:
            invsens_highpass_fNyq = Cinv_highpass_FIRpars.fNyquist
            invsens_highpass_delay = Cinv_highpass_FIRpars.delay_samples
        else:
            invsens_highpass_fNyq = 0
            invsens_highpass_delay = 0
        if A_highpass_FIRpars is not None:
            act_highpass_delay = A_highpass_FIRpars.delay_samples
        else:
            act_highpass_delay = 0

        if plots_directory is not None:
            os.makedirs(plots_directory, exist_ok=True)

            self._verify_act_filters(A_FIRpars, A_highpass_FIRpars,
                                     plots_directory, output_filename)
            self._verify_invsens_filters(Cinv_FIRpars, Cinv_highpass_FIRpars,
                                         plots_directory, output_filename)

            # Compare filters to the model response function
            R_compare_freqs = np.arange(0, 8192.05, 0.05)
            R = self.calcs.compute_response_function(R_compare_freqs[1:])
            D = self.calcs.digital.compute_response(R_compare_freqs[1:])
            RforPlot = np.insert(R, 0, abs(R[0]))
            DforRplot = np.insert(D, 0, abs(D[0]))
            check_td_vs_fd_response(self.inv_sensing, self.inv_sensing_highpass, self.actuation_tst,
                                    self.actuation_pum, self.actuation_uim,
                                    self.actuation_highpass, DforRplot, RforPlot,
                                    invsens_fNyq=Cinv_FIRpars.fNyquist,
                                    invsens_highpass_fNyq=invsens_highpass_fNyq,
                                    act_fNyq=A_FIRpars.fNyquist,
                                    invsens_delay=Cinv_FIRpars.delay_samples,
                                    invsens_highpass_delay=invsens_highpass_delay,
                                    act_delay=A_FIRpars.delay_samples,
                                    act_highpass_delay=act_highpass_delay,
                                    time_delay=1.0 / 16384,
                                    filename="%s/td_vs_fd_response.png" % plots_directory,
                                    plot_title=None, legend=['DARM model', 'FIR filters'])
        # Save output to file
        # Inverse sensing high pass output
        self.invsens_highpass_delay = invsens_highpass_delay
        self.invsens_highpass_sr = invsens_highpass_fNyq * 2
        # Actuation high pass output
        self.actuation_highpass_delay = act_highpass_delay
        # TST actuation output
        self.actuation_tst_delay = A_FIRpars.delay_samples
        self.actuation_tst_sr = A_FIRpars.fNyquist * 2
        # PUM actuation output
        self.actuation_pum_delay = A_FIRpars.delay_samples
        self.actuation_pum_sr = A_FIRpars.fNyquist * 2
        # UIM actuation output
        self.actuation_uim_delay = A_FIRpars.delay_samples
        self.actuation_uim_sr = A_FIRpars.fNyquist * 2
        # Inverse sensing output
        self.inv_sens_delay = Cinv_FIRpars.delay_samples
        self.act_window_type = A_FIRpars.window_type
        self.act_freq_res = A_FIRpars.freq_res
        self.invsens_window_type = Cinv_FIRpars.window_type
        self.invsens_freq_res = Cinv_FIRpars.freq_res

        # Save the filters file
        self._save_filters_file(output_filename, output_dir, exclude_list=self.exclude_from_filters)

    def _compute_calcs_corr(self, freqs):
        """ Compute correction needed for CALCS h(t) output in the frequency domain."""
        if freqs[0] == 0.0:
            calcs_corr_fd = self.calcs.calcs_dtt_calibration(freqs[1:], strain_calib=True)
            calcs_corr_fd = np.insert(calcs_corr_fd, 0, 0)
        else:
            calcs_corr_fd = self.calcs.calcs_dtt_calibration(freqs[1:], strain_calib=True)
        return calcs_corr_fd

    def _generate_calcs_corr_filter(self, CALCS_corr_FIRpars):
        """ Generate all filters for CALCS correction pipeline."""
        # Compute frequency domain model for CALCS correction
        calcs_corr_fd = self._compute_calcs_corr(CALCS_corr_FIRpars.freq_array)
        # Generate FIR filter from frequency-domain model
        [self.calcs_corr_filter, self.calcs_corr_filt_model] = CALCS_corr_FIRpars.create_fir_filter(
                                                                   calcs_corr_fd)

    def _verify_calcs_corr_filter(self, CALCS_corr_FIRpars, plots_directory, output_filename):
        """ Sanity checks on CALCS correction filters."""
        # Sample the model at 8 times the frequency resolution of the filter,
        # and test the filter at that frequency resolution as well.
        # (computeFIRfilters.check_td_vs_fd does that by default.)

        # First generate the calcs correction model for the plot
        calcs_corr_plot_freq = np.arange(0,
                                         CALCS_corr_FIRpars.fNyquist + CALCS_corr_FIRpars.df / 8.0,
                                         CALCS_corr_FIRpars.df / 8.0)
        calcs_corr_fd_for_plot = self._compute_calcs_corr(calcs_corr_plot_freq)
        CALCS_corr_FIRpars.check_td_vs_fd(self.calcs_corr_filter, calcs_corr_fd_for_plot,
                                          filename="%s/calcs_corr_fd_comparison.png"
                                                   % plots_directory,
                                          plot_title="CALCS correction comparison (%s)"
                                                     % output_filename)

    def CALCS_corr(self, output_filename='CALCS_corr.h5',
                   output_dir='.', plots_directory=None):
        """
        CALCS correction FIR filter generation

        Parameters
        ----------
        output_filename : str
            Output filename base
        output_dir : str
            Directory to which to save FIR filters file
        plots_directory : str
            Directory to which to save diagnostic plots

        Returns
        -------
        output_filename, diagnostic plots of filters
        """

        CALCS_corr_FIRpars = FIRfilter(fNyq=self.FIR.calcs_corr_fnyq,
                                       desired_dur=self.FIR.calcs_corr_duration,
                                       highpass_fcut=self.FIR.calcs_corr_highpass_fcut,
                                       window_type=self.FIR.calcs_corr_window_type,
                                       freq_res=self.FIR.calcs_corr_freq_res)

        self._generate_calcs_corr_filter(CALCS_corr_FIRpars)

        if plots_directory is not None:
            os.makedirs(plots_directory, exist_ok=True)

            self._verify_calcs_corr_filter(CALCS_corr_FIRpars, plots_directory, output_filename)

        # Save items as attributes so they are saved to filters file
        self.calcs_corr_delay = CALCS_corr_FIRpars.delay_samples
        self.calcs_corr_sr = CALCS_corr_FIRpars.fNyquist * 2

        # Save the filters file
        self._save_filters_file(output_filename, output_dir, exclude_list=self.exclude_from_filters)


# Perhaps generally useful function for comparing a full set of
# FIR filters to the expected response function model
def check_td_vs_fd_response(invsens_filt, invsens_highpass, TST_filt, PUM_filt, UIM_filt,
                            act_highpass, D, R, invsens_fNyq=8192, invsens_highpass_fNyq=1024,
                            act_fNyq=1024, D_fNyq=8192, R_fNyq=8192, invsens_delay=None,
                            invsens_highpass_delay=None, act_delay=None, act_highpass_delay=None,
                            time_delay=1.0/16384, filename="td_vs_fd_response.png",
                            plot_title="Response Function", legend=['FIR filters', 'DARM model']):
    """
    Checking time-domain vs frequency-domain responses

    Parameters
    ----------
    invsens_filt : array
    invsens_highpass : array
    TST_filt : array-like
    PUM_filt : array-like
    UIM_filt : array-like
    act_highpass : array
    D : array
    R : array
    invsens_fNyq : float, int
    invsens_highpass_fNyq : float, int
    act_fNyq : float, int
    D_fNyq : float, int
    R_fNyq : float, int
    invsens_delay : float, int
    invsens_highpass_delay : float, int
    act_delay : float, int
    act_highpass_delay : float, int
    time_delay : float, int
    filename : str
    plot_title : str
    legend : str, array-like

    Returns
    -------
    plot figure

    """
    if invsens_highpass is None:
        invsens_highpass = []
    if act_highpass is None:
        act_highpass = []

    # If delays are None, assume they are half the length of the filter
    if invsens_delay is None:
        invsens_delay = len(invsens_filt) // 2
    if invsens_highpass_delay is None:
        invsens_highpass_delay = len(invsens_highpass) // 2
    if act_delay is None:
        # This assumes that TST, PUM, and UIM filters are all all the same length
        act_delay = len(TST_filt) // 2
    if act_highpass_delay is None:
        act_highpass_delay = len(act_highpass) // 2

    # Now find frequency responses of each filter
    invsens_fd = freqresp(invsens_filt, delay_samples=invsens_delay)

    invsens_highpass_fd = []
    if any(invsens_highpass):
        invsens_highpass_fd = freqresp(invsens_highpass, delay_samples=invsens_highpass_delay)
    else:
        invsens_highpass_fNyq = 0.0

    TST_fd = freqresp(TST_filt, delay_samples=act_delay)
    PUM_fd = freqresp(PUM_filt, delay_samples=act_delay)
    UIM_fd = freqresp(UIM_filt, delay_samples=act_delay)

    act_highpass_fd = []
    if any(act_highpass):
        act_highpass_fd = freqresp(act_highpass, delay_samples=act_highpass_delay)

    # List of frequency-domain filters and models to manipulate
    fd_list = [[invsens_fd, invsens_highpass_fd, TST_fd, PUM_fd, UIM_fd, act_highpass_fd, D, R],
               [invsens_fNyq, invsens_highpass_fNyq, act_fNyq,
                act_fNyq, act_fNyq, act_fNyq, D_fNyq, R_fNyq],
               [len(invsens_fd), len(invsens_highpass_fd), len(TST_fd), len(PUM_fd), len(UIM_fd),
                len(act_highpass_fd), len(D), len(R)]]
    # Find the maximum Nyquist frequency and pad anything with a lower Nyquist frequency with zeros.
    max_fNyq = max(fd_list[1])
    for i in range(len(fd_list[0])):
        if fd_list[1][i] < max_fNyq and any(fd_list[0][i]):
            length_needed = 1 + int(round(float(fd_list[2][i] - 1) * max_fNyq / fd_list[1][i]))
            if i == 1:
                # The additional inverse sensing filter should be padded with ones instead.
                fd_list[0][i] = np.concatenate((fd_list[0][i],
                                                np.ones(length_needed - fd_list[2][i])))
            else:
                fd_list[0][i] = np.concatenate((fd_list[0][i],
                                                np.zeros(length_needed - fd_list[2][i])))
            fd_list[2][i] = length_needed

    # Now find the finest frequency resolution and upsample everything else to that resolution.
    max_length = max(fd_list[2])
    for i in range(len(fd_list[0])):
        if fd_list[2][i] < max_length and any(fd_list[0][i]):
            resampled = np.zeros(max_length, dtype=np.complex128)
            # linear resampler
            resampled[0] = fd_list[0][i][0]
            resampled[-1] = fd_list[0][i][-1]
            for j in range(1, max_length - 1):
                fdmodel_position = float(j * (fd_list[2][i] - 1)) / (max_length - 1)
                k = int(fdmodel_position)
                after_weight = fdmodel_position - k
                before_weight = 1.0 - after_weight
                resampled[j] = before_weight * fd_list[0][i][k] + after_weight * fd_list[0][i][k+1]
            fd_list[0][i] = resampled

    # Compute a frequency vector
    df = float(max_fNyq) / (max_length - 1)
    frequency = np.arange(0, max_fNyq + df, df)

    # Add in the high-pass filters' frequency response.
    if any(fd_list[0][1]):
        fd_list[0][0] *= fd_list[0][1]
    if any(fd_list[0][5]):
        fd_list[0][2] *= fd_list[0][5]
        fd_list[0][3] *= fd_list[0][5]
        fd_list[0][4] *= fd_list[0][5]

    # Now compute the response of the filters.
    filter_response = fd_list[0][0] + (fd_list[0][2]+fd_list[0][3]+fd_list[0][4]) * fd_list[0][6]

    # Apply a delay if there is one
    if time_delay:
        filter_response *= np.exp(-2.0 * np.pi * 1j * frequency * time_delay)

    # model response
    model_response = fd_list[0][7]

    # Find magnitude and phase, as well as ratios of filters / model
    model_mag = abs(model_response)
    model_phase = np.zeros(len(model_response))
    for i in range(len(model_phase)):
        model_phase[i] = np.angle(model_response[i]) * 180 / np.pi
    filter_mag = abs(filter_response)
    filter_phase = np.zeros(len(filter_response))
    for i in range(len(filter_phase)):
        filter_phase[i] = np.angle(filter_response[i]) * 180 / np.pi

    ratio = []
    assert len(model_response) == len(filter_response)
    for i in range(len(model_response)):
        if model_response[i] != 0.0:
            ratio.append(filter_response[i] / model_response[i])
        else:
            ratio.append(0.0)
    ratio = np.asarray(ratio)
    ratio_mag = abs(ratio)
    ratio_phase = np.zeros(len(ratio))
    for i in range(len(ratio_phase)):
        ratio_phase[i] = np.angle(ratio[i]) * 180.0 / np.pi

    # Make plots
    ymin = pow(10, int(round(np.log10(filter_mag[int(np.ceil(1.0 / df))]))) - 2)
    ymax = pow(10, int(round(np.log10(model_mag[int(np.ceil(1.0 / df))]))) + 2)
    plot(frequency, model_response, frequency, filter_response, freq_min=1,
         freq_max=max(frequency), mag_min=ymin, mag_max=ymax, label=legend,
         title=r'%s' % plot_title, filename=filename)
    return frequency, ratio_mag, ratio_phase


def correctFIRfilter(FIRpars, tdfilt, fdmodel, window_correction_range, save_to_file=None):
    """
    Correct FIR filter production errors induced by windowing,
    and return a compensated version of the frequency-domain model.
    """

    if len(window_correction_range) % 4:
        raise ValueError("correctFIRfilter: Invalid input argument for window_correction_range."
                         " It must be a multiple of 4.")
    for i in range(1, len(window_correction_range)):
        if window_correction_range[i] < window_correction_range[i-1]:
            raise ValueError("correctFIRfilter: Invalid input argument for "
                             "window_correction_range.")
    if type(FIRpars) is not list:
        FIRpars = [FIRpars]
    if type(tdfilt) is not list:
        tdfilt = [tdfilt]

    model = np.asarray(fdmodel)

    fd_from_td = fft.rfft(tdfilt[0])
    fd_from_td *= FIRpars[0].advance_array

    for i in range(1, len(FIRpars)):
        if any(tdfilt[i]):
            factor = fft.rfft(tdfilt[i])
            factor *= FIRpars[i].advance_array
            for j in range(int(FIRpars[i].fNyquist / FIRpars[0].df)):
                fd_from_td[j] *= factor[round(j * FIRpars[0].df / FIRpars[i].df)]

    for i in range(1, len(fd_from_td)):
        if fd_from_td[i] == 0:
            fd_from_td[i] = fd_from_td[i - 1]
    correction = model / fd_from_td

    # Smooth off the correction below the cutoff frequency
    for i in range(FIRpars[0].samples_to_HPcorner):
        j = FIRpars[0].samples_to_HPcorner - 1 - i
        correction[j] = 1.5 * correction[j + 1] - 0.5 * correction[j + 2]

    # Window the result so that it doesn't add kinks to the "corrected" model
    start = 0
    for i in range(len(window_correction_range) // 4):
        rampup_start = int(window_correction_range[4*i+0] / FIRpars[0].df)
        rampup_end = int(window_correction_range[4*i+1] / FIRpars[0].df)
        rampdown_start = int(window_correction_range[4*i+2] / FIRpars[0].df)
        rampdown_end = int(window_correction_range[4*i+3] / FIRpars[0].df)
        for j in range(start, rampup_start):
            correction[j] = 1.0
        hann = np.hanning(3 + 2 * (rampup_end - rampup_start))[1: 1 + rampup_end - rampup_start]
        for j in range(rampup_start, rampup_end):
            correction[j] = correction[j] * hann[j - rampup_start] + 1.0 - hann[j - rampup_start]
        hann = np.hanning(3 + 2 * (rampdown_end
                                   - rampdown_start))[2 + rampdown_end - rampdown_start: -1]
        for j in range(rampdown_start, rampdown_end):
            correction[j] = correction[j] * hann[j - rampdown_start] \
                                + 1.0 - hann[j - rampdown_start]
        start = rampdown_end
    for i in range(start, len(correction)):
        correction[i] = 1.0

    # Multiply the model by the correction
    compensated_model = model * correction

    if save_to_file is not None:
        np.savez(save_to_file, compensated_model=compensated_model)

    return compensated_model
