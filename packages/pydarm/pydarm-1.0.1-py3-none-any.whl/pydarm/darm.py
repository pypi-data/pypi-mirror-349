# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.

import numpy as np

from .model import Model
from .sensing import SensingModel
from .actuation import DARMActuationModel
from .pcal import PcalModel
from .utils import compute_digital_filter_response
from .plot import critique


class DigitalModel(Model):
    """DARM digital filter model object

    """

    def __init__(self, config):
        super().__init__(config, measurement='digital')

        self.digital_response_list = []
        self.digital_frequency_list = []

    def compute_response(self, frequencies):
        """
        Compute DARM digital controller frequency response

        Uses filter ZPK transfer function response from Foton file.

        Parameters
        ----------
        frequencies

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the digital SUS filter

        """

        use_index = False
        idx = 0
        for i, saved_freq_array in enumerate(self.digital_frequency_list):
            if np.array_equiv(np.atleast_1d(frequencies),
                              np.atleast_1d(saved_freq_array)):
                idx = i
                use_index = True
                break

        if use_index:
            response = np.copy(self.digital_response_list[idx])
        else:
            # Emit error if trying to use the old format
            if ((hasattr(self, 'digital_filter_modules_in_use') and not
                 hasattr(self, 'digital_filter_modules'))):
                raise KeyError('Using old name format for filter modules. Please'
                               ' check your configuration string/file and use the'
                               ' updated format to specify filter module'
                               ' parameters.')

            response = np.ones(len(frequencies), dtype='complex128')
            for n in range(len(self.digital_filter_bank)):
                if n == 0:
                    tf, pfilt = compute_digital_filter_response(
                        self.dpath(self.digital_filter_file),
                        self.digital_filter_bank[n],
                        self.digital_filter_modules[n],
                        self.digital_filter_gain[n], frequencies, pfilt=None)
                else:
                    tf = compute_digital_filter_response(
                        self.dpath(self.digital_filter_file),
                        self.digital_filter_bank[n],
                        self.digital_filter_modules[n],
                        self.digital_filter_gain[n], frequencies, pfilt=pfilt)[0]
                response *= tf

            self.digital_response_list.append(np.atleast_1d(response))
            self.digital_frequency_list.append(np.atleast_1d(frequencies))
        return response


class DARMModel(Model):
    """
    DARM model object

    This is a class to set up the model for the DARM loop from a
    configuration file with all the information about where the data is stored

    """

    def __init__(self, config, sensing=None, actuation=None, digital=None, pcal=None):
        super().__init__(config)
        self.sensing = sensing or SensingModel(config)
        self.actuation = actuation or DARMActuationModel(config)
        self.digital = digital or DigitalModel(config)
        self.pcal = pcal
        if not self.pcal and 'pcal' in self._config:
            self.pcal = PcalModel(config)

    def compute_darm_olg(self, frequencies):
        """
        Compute the entire DARM open loop transfer function (see G1501518)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function

        """
        C_response = self.sensing.compute_sensing(frequencies)
        A_response = self.actuation.compute_actuation(frequencies)
        D_response = self.digital.compute_response(frequencies)

        return C_response * A_response * D_response

    def compute_response_function(self, frequencies, sensing_syserr=None,
                                  actuation_syserr_dict=None):
        """
        Compute the entire DARM response transfer function (see G1501518)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        sensing_syserr : `complex`, array-like, optional
            multiplicative factor to include relative sensing systematic error
        actuation_syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        tf : `complex128`, array-like
            transfer function of the DARM closed-loop response

        """

        C_response = self.sensing.compute_sensing(frequencies)
        A_response = self.actuation.compute_actuation(frequencies,
                                                      actuation_syserr_dict)
        D_response = self.digital.compute_response(frequencies)

        if sensing_syserr is not None:
            C_response *= sensing_syserr

        return (1.0/C_response + D_response * A_response)

    def compute_etas(self, frequencies, sensing_syserr=None,
                     actuation_syserr_dict=None):
        """
        Compute multiplicative scaling factor to the response function.
        This returns "eta_R_C", applying sensing systematic error only;
        "eta_R_A", applying actuation systematic error only; and "eta_R",
        applying both sensing and systematic errors.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        sensing_syserr : `complex`, array-like, optional
            multiplicative factor to include relative sensing systematic error
        actuation_syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}, 'yarm': {'PUM': `complex`, array-like}}

        Returns
        -------
        eta_R_c : `complex128`, array-like
            multiplicative scaling factor for the response function, applying the
            sensing systematic errors only
        eta_R_a : `complex128`, array-like
            multiplicative scaling factor for the response function, applying the
            actuation systematic errors only
        eta_R : `complex128`, array-like
            multiplicative scaling factor for the response function, applying both
            sensing and actuation systematic errors

        """

        R = self.compute_response_function(frequencies)

        eta_R_c = self.compute_response_function(frequencies, sensing_syserr=sensing_syserr) / R
        eta_R_a = self.compute_response_function(frequencies,
                                                 actuation_syserr_dict=actuation_syserr_dict) / R
        eta_R = self.compute_response_function(frequencies, sensing_syserr=sensing_syserr,
                                               actuation_syserr_dict=actuation_syserr_dict) / R
        return eta_R_c, eta_R_a, eta_R

    def plot(self, plot_selection='all', freq_min=0.1, freq_max=5000,
             filename=None, ifo='', label=None, style=None, ugf_start=10,
             ugf_end=1000, show=None, **kwargs):
        """
        Make DARM critique plots

        This method produces critique models for 1 or 2 models.

        Parameters
        ----------
        plot_selection : `str`, optional
            Select plot type, one of: 'all' (default), 'optical', 'actuation',
            'clg', 'olg', or 'digital'
        freq_min : `float`, optional
            start frequency
        freq_max : `float`, optional
            end frequency
        filename : `str`, optional
            if given, ALL generated graphs will be saved in one pdf
        ifo : `str`, optional
            if given with a model to plot, it will appear in the
            graph titles
        label : `str` list, optional
            FIXME: what should this be?
        style : `str`, optional
            one of the styles matplotlib has or a user filename with style
        ugf_start : `float`, optional
            start frequency used for the search
        ugf_end : `float`, optional
            end frequency used for the search
        show : `bool`, optional
            if true the plot(s) will show
        **kwargs : optional
            Matplotlib values passed to plots

        """

        critique(self, freq_min=freq_min, freq_max=freq_max, filename=filename, label=label,
                 plot_selection=plot_selection, ifo=ifo, show=show,
                 ugf_start=ugf_start, ugf_end=ugf_end, **kwargs)
