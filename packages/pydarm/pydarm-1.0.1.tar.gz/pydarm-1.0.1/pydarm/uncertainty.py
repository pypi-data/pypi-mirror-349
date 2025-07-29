# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021-2022)
#
# This file is part of pyDARM.

import configparser
import json
import os
import shutil
from copy import deepcopy

import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from tqdm import tqdm

from gwpy.timeseries import TimeSeriesDict as tsd

from .calcs import CALCSModel
from .model import isfloat
from .utils import (
    read_chain_from_hdf5,
    read_gpr_from_hdf5,
    read_response_curves_from_hdf5,
    save_samples_to_txt,
)


class DARMUncertainty(object):

    def __init__(
            self, config, uncertainty_config=None,
            sensing_mcmc_file=None,
            sensing_gpr_file=None,
            actuation_mcmc_files_dict=None,
            actuation_gpr_files_dict=None,
            response_curve_file=None,
    ):
        """
        Initialize a DARMUncertainty object

        Note that any string or path-to-file string in `uncertainty_config`
        will override any uncertainty key value parameters in the `config`
        string or path-to-file

        Parameters
        ----------
        config : file path or string
            INI config
        uncertainty_config : file path or string, optional
            INI config
        sensing_mcmc_file :
        sensing_gpr_file :
        actuation_mcmc_files_dict :
        actuation_gpr_files_dict :
        response_curve_file :
            alternate file paths, overwrites config values
        """

        # Load configuration and set attributes of DARMUncertainty object.
        # Initialize and compute derived data products from configuration.
        # The default is one ini file containing the DARM model parameters and
        # the uncertainty parameters. Alternatively, the uncertainty parameters
        # can be in a separate file from the DARM model parameters. The
        # optional uncertainty will override anything in config
        self._config = None
        self._load_configuration(config)
        self.darm = CALCSModel(config)

        if uncertainty_config is not None:
            self._load_configuration(uncertainty_config)

        if sensing_mcmc_file is not None:
            self.sensing_mcmc_file = sensing_mcmc_file
        if sensing_gpr_file is not None:
            self.sensing_gpr_file = sensing_gpr_file
        if actuation_mcmc_files_dict is not None:
            self.actuation_mcmc_files_dict = actuation_mcmc_files_dict
        if actuation_gpr_files_dict is not None:
            self.actuation_gpr_files_dict = actuation_gpr_files_dict
        if response_curve_file is not None:
            self.response_curve_file = response_curve_file

        # Set the sensing mcmc chain or None
        if hasattr(self, 'sensing_mcmc_file') and self.sensing_mcmc_file != '':
            self.sensing_mcmc_chain = read_chain_from_hdf5(self.sensing_mcmc_file)
        else:
            self.sensing_mcmc_chain = None

        # Set the sensing gpr or None
        if hasattr(self, 'sensing_gpr_file') and self.sensing_gpr_file != '':
            self.sensing_gpr = read_gpr_from_hdf5(self.sensing_gpr_file, 'sensing')
        else:
            self.sensing_gpr = None

        # Set the actuation mcmc list elements, which could be None
        self.actuation_mcmc_dict = {'xarm': {}, 'yarm': {}}
        for idx, arm in enumerate(self.actuation_mcmc_files_dict):
            for n, stage in enumerate(self.actuation_mcmc_files_dict[arm]):
                if self.actuation_mcmc_files_dict[arm][stage] != '':
                    self.actuation_mcmc_dict[arm][stage] = read_chain_from_hdf5(
                        self.actuation_mcmc_files_dict[arm][stage])
                else:
                    self.actuation_mcmc_dict[arm][stage] = None

        # Set the actuation gpr list elements which could be None
        self.actuation_gpr_dict = {'xarm': {}, 'yarm': {}}
        for idx, arm in enumerate(self.actuation_gpr_files_dict):
            for n, stage in enumerate(self.actuation_gpr_files_dict[arm]):
                if self.actuation_gpr_files_dict[arm][stage] != '':
                    meas = f'actuation_{arm[0]}_arm'
                    self.actuation_gpr_dict[arm][stage] = read_gpr_from_hdf5(
                        self.actuation_gpr_files_dict[arm][stage], meas)
                else:
                    self.actuation_gpr_dict[arm][stage] = None

        # In order to account for periods where the uncertainty would
        # nominally be given by a single measurement, we will multiply the
        # previous response function curves onto the new draws.
        # This will inflate the uncertainty as a "stop-gap" measure in
        # periods where we have few measurements of a new model to
        # reliably produce an uncertainty estimate from new measurements
        # alone.
        if (hasattr(self, 'response_curve_file') and
                self.response_curve_file != ''):
            [self.previous_model_response_frequencies,
             self.previous_model_response_curves] = (
                read_response_curves_from_hdf5(self.response_curve_file))
        else:
            self.response_curve_file = None

    def _load_configuration(self, config):
        """Reads configuration and load parameters

        Config can be either file path or configuration string.
        Config interface is stored in `self._config` attribute.

        Parameters
        ----------
        config : file path or string
            INI config
        """

        if self._config is None:
            self._config = configparser.ConfigParser(
                comment_prefixes=('#',), inline_comment_prefixes=('#',))

        if os.path.exists(os.path.normpath(config)):
            with open(os.path.normpath(config)) as f:
                self._config.read_file(f)
        else:
            self._config.read_string(config)

        mcmc_files_dict = {'xarm': {}, 'yarm': {}}
        gpr_files_dict = {'xarm': {}, 'yarm': {}}
        act_delay_sample_dict = {'xarm': {}, 'yarm': {}}
        tdcf_channels_dict = {'sensing': {}, 'xarm': {}, 'yarm': {}}

        for idx, sec in enumerate(self._config):
            if sec == 'reference-model':
                setattr(self, 'model', self._config[sec]['model'])
                setattr(self, 'response_curve_file', self._config.get(
                            sec, 'previous_model_response_curve_file',
                            fallback=''))

            elif sec == 'sensing-measurement':
                setattr(self, 'sensing_mcmc_file', self._config[sec]['mcmc'])
                setattr(self, 'sensing_gpr_file', self._config[sec]['gpr'])

            # Actuation measurement files
            elif 'arm-measurement' in sec:
                arm = ''.join(sec.split('-')[0:2])
                for n, (key, value) in enumerate(self._config[sec].items()):
                    stage = key.split('_')[0].upper()
                    if 'mcmc' in key:
                        mcmc_files_dict[arm][stage] = value
                    elif 'gpr' in key:
                        gpr_files_dict[arm][stage] = value
                    else:
                        act_delay_sample_dict[arm][stage] = value

            # TDCF channels
            elif sec == 'sensing-tdcf' or sec == 'x-arm-tdcf' or sec == 'y-arm-tdcf':
                if 'arm' not in sec:
                    sys = 'sensing'
                else:
                    sys = ''.join(sec.split('-')[0:2])
                for n, (key, value) in enumerate(self._config[sec].items()):
                    if isfloat(value):
                        tdcf_channels_dict[sys][key] = float(value)
                    else:
                        tdcf_channels_dict[sys][key] = value

            # TDCF data type, duration, and line uncertainty threshold
            elif sec == 'tdcf-data':
                setattr(self, 'frametype', self._config[sec]['frametype'])
                setattr(self, 'duration', float(self._config[sec]['duration']))

            elif sec == 'hoft-tdcf-data-application':
                tdcf_data_application = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    tdcf_data_application[key] = \
                        bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'hoft_tdcf_application', tdcf_data_application)

            elif sec == 'sample-tdcf':
                sample_tdcf = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    sample_tdcf[key] = \
                        bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'sample_tdcf', sample_tdcf)

            elif sec == 'pcal':
                pcal = {}
                for n, (key, value) in enumerate(self._config[sec].items()):
                    if (key == 'sys_err' or key == 'sys_unc') and value != '':
                        pcal[key] = float(value)
                    elif key == 'sys_err' and value == '':
                        pcal[key] = 1
                    elif key == 'sys_unc' and value == '':
                        pcal[key] = 0
                    elif key == 'sample':
                        pcal[key] = \
                            bool(value.lower() in ('yes', 'y', 'true', 't', '1'))
                setattr(self, 'pcal', pcal)

        setattr(self, 'actuation_mcmc_files_dict', mcmc_files_dict)
        setattr(self, 'actuation_gpr_files_dict', gpr_files_dict)
        setattr(self, 'act_delay_sample_dict', act_delay_sample_dict)
        setattr(self, 'tdcf_channels_dict', tdcf_channels_dict)

    def _channel_list_from_dict(self):
        """
        This method creates a list from the TDCF channels dict

        Parameters
        ----------
        Returns
        -------
        channels : `list`
            Channels of the TDCFs
        """
        channels = []
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if not isfloat(ch) and par != 'pcal_arm':
                    channels.append(ch)

        return channels

    def tdcf_channel_list(self):
        """return the TDCF channel list, with <IFO>: prefix

        """
        channels = []
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if not isfloat(ch) and par != 'pcal_arm':
                    channels.append(f'{self.darm.name}:{ch}')
        return channels

    def _query_data(self, gpstime, data=None):
        """
        Get the data from either a gwpy.timeseries.TimeSeriesDict object
        or by querying for the data

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-self.duration/2, gpstime+self.duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        TimeSeriesDict
            gwpy object containing the data
        """

        # Full channel list
        chans = self._channel_list_from_dict()
        chans_copy = chans.copy()
        for idx, ch in enumerate(chans):
            chans_copy[idx] = f'{self.darm.name}:{ch}'

        # Query for data unless data is passed
        if (data is not None and
                data.span[0] == gpstime - self.duration/2 and
                data.span[1] == gpstime + self.duration/2 and
                set(chans_copy) <= set(list(data.keys()))):
            pass
        else:
            if data is not None:
                print('WARNING:')
                print('Data object passed does not match the timespan or channel list required')
            data = self._get_gwpy_data(gpstime, channels=chans,
                                       duration=self.duration,
                                       frametype=self.frametype)

        return data

    def _get_gwpy_data(self, gpstime, duration=130,
                       channels=['CAL-CS_TDEP_KAPPA_C_OUTPUT',
                                 'CAL-CS_TDEP_F_C_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT',
                                 'CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT',
                                 'CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY',
                                 'CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY',
                                 'CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY'],
                       frametype='R'):
        """
        Get the data using gwpy

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        duration : `int`, optional
            duration of data to query in seconds
        channels : str `list`, optional
            list of channel names without the '<IFO>:' part
        frametype : str
            frametype without the '<IFO>_' part

        Returns
        -------
        TimeSeriesDict
            gwpy object containing the data
        """

        channels_copy = channels.copy()
        for idx, ch in enumerate(channels):
            channels_copy[idx] = f'{self.darm.name}:{ch}'

        frametype = f'{self.darm.name}_{frametype}'
        gpsStart = gpstime - self.duration / 2
        gpsEnd = gpstime + self.duration / 2

        return tsd.get(channels_copy, gpsStart, gpsEnd, frametype=frametype)

    def tdcf_mean_values(self, gpstime, data=None):
        """
        Compute the mean values of the TDCF channels

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        sensing : `float`, array-like
            kappa_c and f_cc in that order; zero if no channel provided
        actuation_x_arm : `float`, array-like
            kappa_uim, kappa_pum, kappa_tst in that order; zero if no channel provided
        actuation_y_arm : `float`, array-like
            kappa_uim, kappa_pum, kappa_tst in that order; zero if no channel provided
        """
        # Query for data
        data = self._query_data(gpstime, data=data)

        sensing = np.zeros(2)
        actuation_x_arm = np.zeros(3)
        actuation_y_arm = np.zeros(3)

        # Estimated TDCF values
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if par == 'pcal_arm':
                    continue
                elif isfloat(ch):
                    tdcf_mean = ch
                else:
                    tdcf_mean = np.mean(data[f'{self.darm.name}:{ch}'].value)
                if subsys == 'sensing':
                    if par == 'kappa_c':
                        sensing[0] = tdcf_mean
                    elif par == 'f_cc':
                        sensing[1] = tdcf_mean
                if subsys == 'xarm':
                    if par == 'kappa_uim':
                        actuation_x_arm[0] = tdcf_mean
                    elif par == 'kappa_pum':
                        actuation_x_arm[1] = tdcf_mean
                    elif par == 'kappa_tst':
                        actuation_x_arm[2] = tdcf_mean
                if subsys == 'yarm':
                    if par == 'kappa_uim':
                        actuation_y_arm[0] = tdcf_mean
                    elif par == 'kappa_pum':
                        actuation_y_arm[1] = tdcf_mean
                    elif par == 'kappa_tst':
                        actuation_y_arm[2] = tdcf_mean

        return sensing, actuation_x_arm, actuation_y_arm

    def sample_line_uncertainty(self, gpstime, data=None):
        """
        Sample the calibration line uncertainty

        Parameters
        ----------
        gpstime : int
            GPS time at the point of interest. queried data will be
            [gpstime-duration/2, gpstime+duration/2)
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        this_cal_sensing : float
        this_cal_sus_x : `float`, array-like
        this_cal_sus_y : `float`, array-like
        """
        # Query for data
        data = self._query_data(gpstime, data=data)

        # Estimated uncertainties of lines
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if par == 'pcal_arm':
                    continue
                elif isfloat(ch):
                    unc_mean = ch
                else:
                    unc_mean = np.mean(data[f'{self.darm.name}:{ch}'].value)

                if subsys == 'sensing':
                    if par == 'pcal2_unc':
                        pcal2_unc = unc_mean
                        this_cal_line_pcal_2 = np.random.normal(1, pcal2_unc)
                if subsys == 'xarm':
                    if par == 'uim_unc':
                        kappa_uim_unc_x = unc_mean
                        this_cal_line_u_x = np.random.normal(1, kappa_uim_unc_x)
                    elif par == 'pum_unc':
                        kappa_pum_unc_x = unc_mean
                        this_cal_line_p_x = np.random.normal(1, kappa_pum_unc_x)
                    elif par == 'tst_unc':
                        kappa_tst_unc_x = unc_mean
                        this_cal_line_t_x = np.random.normal(1, kappa_tst_unc_x)
                    elif par == 'pcal1_unc':
                        pcal1_unc_x = unc_mean
                        this_cal_line_pcal_1_x = np.random.normal(1, pcal1_unc_x)
                if subsys == 'yarm':
                    if par == 'uim_unc':
                        kappa_uim_unc_y = unc_mean
                        this_cal_line_u_y = np.random.normal(1, kappa_uim_unc_y)
                    elif par == 'pum_unc':
                        kappa_pum_unc_y = unc_mean
                        this_cal_line_p_y = np.random.normal(1, kappa_pum_unc_y)
                    elif par == 'tst_unc':
                        kappa_tst_unc_y = unc_mean
                        this_cal_line_t_y = np.random.normal(1, kappa_tst_unc_y)
                    elif par == 'pcal1_unc':
                        pcal1_unc_y = unc_mean
                        this_cal_line_pcal_1_y = np.random.normal(1, pcal1_unc_y)

        # If no CAL line uncertainty channel was given, set scaling to be = 1
        # TODO: probably cleaner way to do this
        if 'this_cal_line_pcal_1_x' not in locals():
            this_cal_line_pcal_1_x = 1.0
        if 'this_cal_line_pcal_1_y' not in locals():
            this_cal_line_pcal_1_y = 1.0
        if 'this_cal_line_pcal_2' not in locals():
            this_cal_line_pcal_2 = 1.0
        if 'this_cal_line_u_x' not in locals():
            this_cal_line_u_x = 1.0
        if 'this_cal_line_p_x' not in locals():
            this_cal_line_p_x = 1.0
        if 'this_cal_line_t_x' not in locals():
            this_cal_line_t_x = 1.0
        if 'this_cal_line_u_y' not in locals():
            this_cal_line_u_y = 1.0
        if 'this_cal_line_p_y' not in locals():
            this_cal_line_p_y = 1.0
        if 'this_cal_line_t_y' not in locals():
            this_cal_line_t_y = 1.0

        this_cal_sensing = this_cal_line_pcal_2

        this_cal_sus_x = np.array([
            this_cal_line_u_x, this_cal_line_p_x, this_cal_line_t_x,
            this_cal_line_pcal_1_x])

        this_cal_sus_y = np.array([
            this_cal_line_u_y, this_cal_line_p_y, this_cal_line_t_y,
            this_cal_line_pcal_1_y])

        return this_cal_sensing, this_cal_sus_x, this_cal_sus_y

    @staticmethod
    def sample_pcal_unc(err=1, unc=0.005):
        """
        Sample PCAL uncertainty

        Parameters
        ----------
        err : `float`, optional
        unc : `float`, optional

        Returns
        -------
        `float`
        """
        return np.random.normal(err, unc)

    @staticmethod
    def get_model_pars(model):
        """
        Extract the main fitted parameters from MCMCs into structures

        Parameters
        ----------
        model : pydarm.darm.DARMModel object

        Returns
        -------
        sensing_pars : dict
            dictionary of the sensing parameters that the MCMC posteriors would
            impact
        act_pars : dict
            dictionary of the actuation parameters that the MCMC posteriors
            would impact
        """
        sensing_pars = {'gain': model.sensing.coupled_cavity_optical_gain,
                        'f_cc': model.sensing.coupled_cavity_pole_frequency,
                        'f_s': model.sensing.detuned_spring_frequency,
                        'Q': model.sensing.detuned_spring_q,
                        'single_pole_delay_corr':
                            model.sensing.single_pole_approximation_delay_correction}

        act_pars = {'xarm': {}, 'yarm': {}}
        if model.actuation.xarm is not None and model.actuation.xarm.uim_npa != '':
            act_pars['xarm']['UIM'] = [model.actuation.xarm.uim_npa]
            if model.actuation.xarm.uim_delay != '':
                act_pars['xarm']['UIM'].append(model.actuation.xarm.uim_delay)
        if model.actuation.xarm is not None and model.actuation.xarm.pum_npa != '':
            act_pars['xarm']['PUM'] = [model.actuation.xarm.pum_npa]
            if model.actuation.xarm.pum_delay != '':
                act_pars['xarm']['PUM'].append(model.actuation.xarm.pum_delay)
        if model.actuation.xarm is not None and model.actuation.xarm.tst_npv2 != '':
            act_pars['xarm']['TST'] = [model.actuation.xarm.tst_npv2]
            if model.actuation.xarm.tst_delay != '':
                act_pars['xarm']['TST'].append(model.actuation.xarm.tst_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.uim_npa != '':
            act_pars['yarm']['UIM'] = [model.actuation.yarm.uim_npa]
            if model.actuation.yarm.uim_delay != '':
                act_pars['yarm']['UIM'].append(model.actuation.yarm.uim_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.pum_npa != '':
            act_pars['yarm']['PUM'] = [model.actuation.yarm.pum_npa]
            if model.actuation.yarm.pum_delay != '':
                act_pars['yarm']['PUM'].append(model.actuation.yarm.pum_delay)
        if model.actuation.yarm is not None and model.actuation.yarm.tst_npv2 != '':
            act_pars['yarm']['TST'] = [model.actuation.yarm.tst_npv2]
            if model.actuation.yarm.tst_delay != '':
                act_pars['yarm']['TST'].append(model.actuation.yarm.tst_delay)

        return sensing_pars, act_pars

    @staticmethod
    def sample_gpr(gpr, frequencies, n_trials=1):
        """
        Sample from the GPR instance where there are 4 parameters:
        - model configuration string (str)
        - best fit curve of the data (complex, array-like)
        - covariance matrix (float, array-like)
        - frequencies (float, array-like)

        Parameters
        ----------
        gpr : list
            GPR list instance as described above
        frequencies : `float`, array-like
            list of frequencies to sample the GPR; if this is different than
            what the GPR was computed on, then this method will interpolate
            to the new values using linear interpolation

        Returns
        -------
        this_gpr : `complex`, array-like
            sampled GPR function
        """

        rng_state = np.random.get_state()
        gpr_mag_samples = np.random.multivariate_normal(
            np.abs(gpr[1]), gpr[2], size=n_trials).T
        np.random.set_state(rng_state)
        gpr_pha_samples = np.random.multivariate_normal(
            np.angle(gpr[1]), gpr[2], size=n_trials).T
        gpr_samples = (gpr_mag_samples * np.exp(1j * gpr_pha_samples))

        # interpolate to given frequencies
        gpr_samples = interp1d(gpr[3], gpr_samples.T)(frequencies)

        return gpr_samples

    def sample_response(self, gpstime, frequencies, n_trials=1, data=None,
                        supplemental_sensing_gpr=None):
        """
        This method samples the response function at a specific GPS time one
        at a time. Call this method multiple times in order to get an estimate
        of the overall error and uncertainty

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required
        supplemental_sensing_gpr : `str`, optional
            Path to file of an additional sensing function GPR to apply when
            sampling

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function
        data : `gwpy.timeseries.TimeSeriesDict` object
            object containing the queried channel data
        sensing_pars : dict
            dictionary of sesing parameters for this sample (gain, f_cc, f_s,
            Q, and tau_c (the residual delay)
        act_pars : dict
            dictionary of actuation parameters for this sample. Each entry
            for an arm and stage is a list of: gain, tau_i (the residual delay)
        this_sensing_syserr : `complex128`, array-like
            sample for this sensing function GPR
        act_syserr_dict : dict
            dictionary of samples for this arm and stage for actuation GPR
        """

        # Check that the frequencies in the GPR files are the same as what is
        # requested. If not print a warning that interpolation will be used
        if self.sensing_gpr is not None:
            if not np.array_equal(frequencies, self.sensing_gpr[3]):
                print('NOTE: chosen frequencies are not commensurate with sensing GPR. '
                      'Interpolation is used')
        for idx, arm in enumerate(self.actuation_gpr_dict):
            for n, stage in enumerate(self.actuation_gpr_dict[arm]):
                if self.actuation_gpr_dict[arm][stage] is not None:
                    if not np.array_equal(frequencies, self.actuation_gpr_dict[arm][stage][3]):
                        print(f'NOTE: chosen frequencies are not commensurate with {arm} {stage} '
                              'GPR. Interpolation is used')

        # Sample sensing MCMC here; we'll be sampling the actuation MCMC later
        if self.sensing_mcmc_chain is not None:
            sensing_mcmc_idxes = np.random.randint(
                low=0, high=len(self.sensing_mcmc_chain[4]), size=n_trials)
            sensing_pars_samples = self.sensing_mcmc_chain[4][sensing_mcmc_idxes]
        else:
            sensing_pars_samples = np.outer(np.ones(n_trials), [
                self.darm.sensing.coupled_cavity_optical_gain,
                self.darm.sensing.coupled_cavity_pole_frequency,
                self.darm.sensing.detuned_spring_frequency,
                self.darm.sensing.detuned_spring_q,
                0])

        # Sample sensing GPR; we'll be sampling the actuation GPR later
        if self.sensing_gpr is not None:
            sensing_syserr_samples = self.sample_gpr(
                self.sensing_gpr, frequencies, n_trials=n_trials)
        else:
            sensing_syserr_samples = np.ones((n_trials, len(frequencies)), dtype='complex128')

        # If a thermalization was passed, read it and sample
        if supplemental_sensing_gpr is not None:
            supplemental_sensing_samples = self.sample_gpr(
                self.read_gpr_from_hdf5(supplemental_sensing_gpr, 'sensing'),
                frequencies,
                n_trials=n_trials)
            sensing_syserr_samples *= supplemental_sensing_samples

        # Sample gpr if a file was given
        act_pars_samples = {'xarm': {}, 'yarm': {}}
        act_syserr_dict = {'xarm': {}, 'yarm': {}}
        arms = list(act_syserr_dict.keys())
        kappa_a_label = ['TOP', 'UIM', 'PUM', 'TST']
        output_matrix = self.darm.actuation.darm_output_matrix_values()
        for n in range(len(output_matrix[:, 0])):
            for m in range(len(output_matrix[0, :])):
                if output_matrix[n, m] != 0:
                    arm = arms[n]
                    stage = kappa_a_label[m]

                    act_pars_samples[arm][stage] = []

                    if self.actuation_gpr_dict[arm][stage] is not None:
                        this_actuation_syserr = self.sample_gpr(
                            self.actuation_gpr_dict[arm][stage],
                            frequencies, n_trials=n_trials)
                    else:
                        this_actuation_syserr = np.ones((n_trials, len(frequencies)),
                                                        dtype='complex128')

                    act_syserr_dict[arm][stage] = this_actuation_syserr

        # Query for data unless data is passed
        data = self._query_data(gpstime, data=data)

        tf_array = np.ones((n_trials, len(frequencies)), dtype='complex128')
        for n_trial in tqdm(range(n_trials)):
            # Make copy of darm because we don't want to edit the original
            darm_copy = deepcopy(self.darm)

            # Estimated TDCF values and uncertainties of lines
            sensing_tdcf, sus_x_tdcf, sus_y_tdcf = \
                self.tdcf_mean_values(gpstime, data=data)
            this_cal_sensing, this_cal_sus_x, this_cal_sus_y = \
                self.sample_line_uncertainty(gpstime, data=data)

            # Sampled actuator TDCF values.
            # This part just scales the reference value by the sampled uncertainty
            # of the calibration lines (if requested) and the mean of the TDCF.
            # Later, we will bring in the MCMC sampling by dividing out the
            # reference value and multiply in the MCMC sample (again, if requested)
            if self.sample_tdcf['kappa_uim']:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.uim_npa != '':
                    darm_copy.actuation.xarm.uim_npa *= (this_cal_sus_x[0] *
                                                         this_cal_sus_x[3] *
                                                         sus_x_tdcf[0])
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.uim_npa != '':
                    darm_copy.actuation.yarm.uim_npa *= (this_cal_sus_y[0] *
                                                         this_cal_sus_y[3] *
                                                         sus_y_tdcf[0])
            else:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.uim_npa != '':
                    darm_copy.actuation.xarm.uim_npa *= sus_x_tdcf[0]
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.uim_npa != '':
                    darm_copy.actuation.yarm.uim_npa *= sus_y_tdcf[0]
            if self.sample_tdcf['kappa_pum']:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.pum_npa != '':
                    darm_copy.actuation.xarm.pum_npa *= (this_cal_sus_x[1] *
                                                         this_cal_sus_x[3] *
                                                         sus_x_tdcf[1])
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.pum_npa != '':
                    darm_copy.actuation.yarm.pum_npa *= (this_cal_sus_y[1] *
                                                         this_cal_sus_y[3] *
                                                         sus_y_tdcf[1])
            else:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.pum_npa != '':
                    darm_copy.actuation.xarm.pum_npa *= sus_x_tdcf[1]
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.pum_npa != '':
                    darm_copy.actuation.yarm.pum_npa *= sus_y_tdcf[1]
            if self.sample_tdcf['kappa_tst']:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.tst_npv2 != '':
                    darm_copy.actuation.xarm.tst_npv2 *= (this_cal_sus_x[2] *
                                                          this_cal_sus_x[3] *
                                                          sus_x_tdcf[2])
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.tst_npv2 != '':
                    darm_copy.actuation.yarm.tst_npv2 *= (this_cal_sus_y[2] *
                                                          this_cal_sus_y[3] *
                                                          sus_y_tdcf[2])
            else:
                if darm_copy.actuation.xarm is not None and darm_copy.actuation.xarm.tst_npv2 != '':
                    darm_copy.actuation.xarm.tst_npv2 *= sus_x_tdcf[2]
                if darm_copy.actuation.yarm is not None and darm_copy.actuation.yarm.tst_npv2 != '':
                    darm_copy.actuation.yarm.tst_npv2 *= sus_y_tdcf[2]

            # kappa_C and f_cc estimated to compute normalized to reference optical
            # response
            # First get the sensing calibration line frequency
            sensing_line_freq = self.darm.calcs.cal_line_sens_pcal_frequency
            # Get the residual sensing C_res, which is everything except the
            # kappa_C and the frequency dependence
            EP4 = (darm_copy.sensing.coupled_cavity_optical_gain *
                   darm_copy.sensing.sensing_residual(
                       np.asarray([sensing_line_freq]))[0])
            # Calculate the normalized optical response and include kappa_C
            opt_zpk = darm_copy.sensing.optical_response(
                sensing_tdcf[1], darm_copy.sensing.detuned_spring_frequency,
                darm_copy.sensing.detuned_spring_q,
                darm_copy.sensing.is_pro_spring)
            opt = (sensing_tdcf[0] *
                   signal.freqresp(opt_zpk, 2*np.pi*sensing_line_freq)[1][0])
            # Compute the sensing function at the calibration line frequency
            C_CalLineP2 = EP4 * opt

            # TODO: need a way to confirm the EPICS records used to compute the TDCFs
            #       are the same is what is computed here
            EP5 = darm_copy.digital.compute_response(
                np.asarray([sensing_line_freq]))[0]
            # This is nominally EP6 + EP7 + EP8 since we've already multiplied in
            # the actuator TDCFs above
            A_CalLineP2 = darm_copy.actuation.compute_actuation(
                np.asarray([sensing_line_freq]))[0]
            # Get the Pcal correction factor, assuming both DARM and Pcal are read
            # from the CALCS model. This means we don't need extra corrections to
            # propogate back to the end station
            EP9 = darm_copy.pcal.compute_pcal_correction(
                np.asarray([sensing_line_freq]), endstation=True)[0]
            # Compute "(d_err/x_pc)**(-1)" from reference model EPICS records and
            # mean TDCF values
            kappaC_FC_CalLineP2 = (1.0/C_CalLineP2 + EP5 * A_CalLineP2) / EP9
            # Compute "S" for this sample, T1700106-v10 eq 46
            this_S = 1.0/(EP4 * EP9 * kappaC_FC_CalLineP2*this_cal_sensing -
                          EP4 * EP5 * A_CalLineP2)

            # Sampled sensing TDCF values
            if self.sample_tdcf['kappa_c']:
                this_kappa_c = np.abs(this_S)**2/np.real(this_S)
            else:
                this_kappa_c = sensing_tdcf[0]
            if self.sample_tdcf['f_cc']:
                this_f_cc = -np.real(this_S)/np.imag(this_S)*sensing_line_freq
            else:
                this_f_cc = sensing_tdcf[1]

            # Scale sensing
            # For optical gain, scale the sampled MCMC value (absolute) by the
            # sampled TDCF value (relative)
            # H_c,sample(t) = kappa_c,draw(t) x H_c,draw(0)
            # where kappa_c can have a central value different than 1.
            # For cavity pole, the situation is a bit more complicated because we
            # only have absolute numerical values so we need to construct the
            # analagous "kappa" value
            # f_cc,sample(t) = [f_cc,draw(t)/f_cc,MAP] x f_cc,draw(0)
            # where the ratio in brackets [ ] can have a central value offset from
            # unity.
            # Spring frequency, Q, and residual time delay are only sampled from
            # the MCMC, since we do not have reliable TDCF values
            this_sensing = np.atleast_2d(sensing_pars_samples)[n_trial]
            darm_copy.sensing.coupled_cavity_optical_gain = this_kappa_c * this_sensing[0]
            darm_copy.sensing.coupled_cavity_pole_frequency = (
                (this_f_cc/darm_copy.sensing.coupled_cavity_pole_frequency) *
                this_sensing[1])
            darm_copy.sensing.detuned_spring_frequency = this_sensing[2]
            darm_copy.sensing.detuned_spring_q = this_sensing[3]
            darm_copy.sensing.single_pole_approximation_delay_correction += \
                this_sensing[4]

            # Sample and scale actuation from the MCMC; build syserr dict
            for n in range(len(output_matrix[:, 0])):
                for m in range(len(output_matrix[0, :])):
                    if output_matrix[n, m] != 0:
                        arm = arms[n]
                        stage = kappa_a_label[m]

                        # Sample MCMC if a file was given
                        if self.actuation_mcmc_dict[arm][stage] is not None:
                            # get random integer from 0 to length of the MCMC chain - 1
                            actuation_mcmc_idx = np.random.randint(
                                low=0, high=len(self.actuation_mcmc_dict[arm][stage][4]))
                            mcmc_sample_gain = \
                                self.actuation_mcmc_dict[arm][stage][4][actuation_mcmc_idx][0]
                            mcmc_sample_delay = 0

                            # if sampling the residual MCMC delay
                            if ((delay_stage := self.act_delay_sample_dict[arm].get(stage, '')) !=
                                    ''):
                                if delay_stage == stage:
                                    mcmc_sample_delay = (
                                        self.actuation_mcmc_dict[arm][stage][4][
                                            actuation_mcmc_idx][1])
                                else:
                                    idx = np.random.randint(
                                        low=0,
                                        high=len(self.actuation_mcmc_dict[arm][delay_stage][4]))
                                    mcmc_sample_delay = (
                                        self.actuation_mcmc_dict[arm][delay_stage][4][idx][1])

                            act_pars_samples[arm][stage].append(
                                [mcmc_sample_gain, mcmc_sample_delay])

                            # Assignments to darm_copy object
                            if n == 0 and m == 1:
                                darm_copy.actuation.xarm.uim_npa *= (
                                    mcmc_sample_gain / self.darm.actuation.xarm.uim_npa)
                                darm_copy.actuation.xarm.uim_delay += mcmc_sample_delay
                            elif n == 0 and m == 2:
                                darm_copy.actuation.xarm.pum_npa *= (
                                    mcmc_sample_gain / self.darm.actuation.xarm.pum_npa)
                                darm_copy.actuation.xarm.pum_delay += mcmc_sample_delay
                            elif n == 0 and m == 3:
                                darm_copy.actuation.xarm.tst_npv2 *= (
                                    mcmc_sample_gain / self.darm.actuation.xarm.tst_npv2)
                                darm_copy.actuation.xarm.tst_delay += mcmc_sample_delay
                            elif n == 1 and m == 1:
                                darm_copy.actuation.yarm.uim_npa *= (
                                    mcmc_sample_gain / self.darm.actuation.yarm.uim_npa)
                                darm_copy.actuation.yarm.uim_delay += mcmc_sample_delay
                            elif n == 1 and m == 2:
                                darm_copy.actuation.yarm.pum_npa *= (
                                    mcmc_sample_gain / self.darm.actuation.yarm.pum_npa)
                                darm_copy.actuation.yarm.pum_delay += mcmc_sample_delay
                            elif n == 1 and m == 3:
                                darm_copy.actuation.yarm.tst_npv2 *= (
                                    mcmc_sample_gain / self.darm.actuation.yarm.tst_npv2)
                                darm_copy.actuation.yarm.tst_delay += mcmc_sample_delay

            # Recall this samples' parameters
            sensing_pars, act_pars = self.get_model_pars(darm_copy)

            # Since the residual sensing delay from the MCMC was included in the
            # single pole approximation delay correction (adding to it), we should
            # subtract the reference model delay correction so that we have the
            # sampled tau_c
            this_sensing_single_pole_corr = sensing_pars.pop('single_pole_delay_corr')
            sensing_pars['tau_c'] = (
                this_sensing_single_pole_corr -
                self.darm.sensing.single_pole_approximation_delay_correction)

            # Collect the GPR samples
            this_sensing_syserr = sensing_syserr_samples[n_trial]
            this_act_syserr_dict = {'xarm': {}, 'yarm': {}}
            for n in range(len(output_matrix[:, 0])):
                for m in range(len(output_matrix[0, :])):
                    if output_matrix[n, m] != 0:
                        arm = arms[n]
                        stage = kappa_a_label[m]
                        this_act_syserr_dict[arm][stage] = act_syserr_dict[arm][stage][n_trial]

            # Compute the response
            tf = darm_copy.compute_response_function(
                frequencies, this_sensing_syserr, this_act_syserr_dict)

            # Pcal uncertainty
            if self.pcal['sample']:
                pcal_unc = self.sample_pcal_unc(self.pcal['sys_err'], self.pcal['sys_unc'])
            else:
                pcal_unc = self.pcal['sys_err']

            tf /= pcal_unc
            tf_array[n_trial] *= tf

        return tf_array, data, sensing_pars_samples, act_pars_samples, \
            sensing_syserr_samples, act_syserr_dict

    def nominal_response(self, gpstime, frequencies, data=None):
        """
        This method computes the response function of a model at a specified
        GPS time, and, depending on whether the time-dependent correction
        factors were applied at the time, applies those TDCFs to the model so
        that the response function is corrected for those changes at a specific
        GPS time

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the sensing function
        data : `gwpy.timeseries.TimeSeriesDict` object
            object containing the queried channel data
        """

        # Make copy of darm because we don't want to edit the original
        darm_copy = deepcopy(self.darm)

        # Query for data unless data is passed
        data = self._query_data(gpstime, data=data)

        # Estimated TDCF values
        # A reminder that the optical gain and gains of actuators are scaled by
        # a multiplicative factor whereas the cavity pole is simply modified to
        # a new value
        for idx, (subsys, val) in enumerate(self.tdcf_channels_dict.items()):
            for idx2, (par, ch) in enumerate(self.tdcf_channels_dict[subsys].items()):
                if (par in self.hoft_tdcf_application and
                        self.hoft_tdcf_application[par]):
                    if isfloat(ch):
                        tdcf_mean = ch
                    else:
                        tdcf_mean = np.mean(data[f'{darm_copy.name}:{ch}'].value)
                    if par == 'f_cc':
                        darm_copy.sensing.coupled_cavity_pole_frequency = tdcf_mean
                    elif par == 'kappa_c':
                        darm_copy.sensing.coupled_cavity_optical_gain *= tdcf_mean
                    elif par == 'kappa_uim':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.uim_npa *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.uim_npa *= tdcf_mean
                    elif par == 'kappa_pum':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.pum_npa *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.pum_npa *= tdcf_mean
                    elif par == 'kappa_tst':
                        if subsys == 'xarm':
                            darm_copy.actuation.xarm.tst_npv2 *= tdcf_mean
                        elif subsys == 'yarm':
                            darm_copy.actuation.yarm.tst_npv2 *= tdcf_mean

        # For sensing, we have assumed that the time delay is essentially zero
        # within the normal uncertainty of measurements. Sometimes the MCMC
        # will indicate a value that is deviating from zero, but we don't
        # include it in any FIR filter generation or when we divide out the
        # TDCF-corrected model to get residuals for GPR calculations. So what
        # we do is include the delay here from the MAP values. The situation
        # is similar with the actuation delay, we assume it is zero or that the
        # model has been adjusted to account for an unknown delay, so any
        # residual delay in the MCMC fitting is not included in the model or
        # FIR filter generation or GPR calculations
        if self.sensing_mcmc_chain is not None:
            delay_map = np.median(self.sensing_mcmc_chain[4][:, 4])
            darm_copy.sensing.single_pole_approximation_delay_correction += (
                delay_map)
        output_matrix = darm_copy.actuation.darm_output_matrix_values()
        arms = ['xarm', 'yarm']
        stages = ['TOP', 'UIM', 'PUM', 'TST']
        # For each of the actuation arms and stages, check that it is used in
        # the model of DARM loop and then look to see if the MCMC for
        # that stage is given and then the delay MAP value will be based on
        # the value of <stage>_delay_sample in the ini file
        # (which is set into a dictionary act_delay_sample_dict within this
        # class instance)
        for arm in arms:
            for stage in stages:
                if output_matrix[arms.index(arm), stages.index(stage)] != 0:
                    if (self.actuation_mcmc_dict[arm][stage] is not None and
                            (delay_stage := self.act_delay_sample_dict[arm].get(stage, '')) != ''):
                        # The delay MAP value is determined by the setting of
                        # <stage>_delay_sample. Ex.: tst_delay_sample = TST
                        # will get the median of the TST posterior samples
                        # from the TST HDF5 file. If tst_delay_sample = PUM
                        # then the TST stage delay MAP will be assigned the
                        # median of the PUM stage
                        if delay_stage == stage:
                            delay_map = np.median(
                                self.actuation_mcmc_dict[arm][stage][4][:, 1])
                        else:
                            delay_map = np.median(
                                self.actuation_mcmc_dict[arm][delay_stage][4][:, 1])
                        if arm == 'xarm':
                            setattr(darm_copy.actuation.xarm, f'{stage.lower()}_delay',
                                    getattr(darm_copy.actuation.xarm,
                                            f'{stage.lower()}_delay') + delay_map)
                        elif arm == 'yarm':
                            setattr(darm_copy.actuation.yarm, f'{stage.lower()}_delay',
                                    getattr(darm_copy.actuation.yarm,
                                            f'{stage.lower()}_delay') + delay_map)

        tf = darm_copy.compute_response_function(frequencies)

        if ('pcal_sys_err' in self.hoft_tdcf_application and
                self.hoft_tdcf_application['pcal_sys_err']):
            tf /= self.pcal['sys_err']

        return tf, data

    def compute_response_uncertainty(self, gpstime, frequencies, trials=1000,
                                     data=None, shift_sample_tf=None,
                                     save_to_file_h5=None,
                                     save_to_file_txt=None,
                                     seed=None,
                                     **kwargs):
        """
        This method samples the response function uncertainty a number of times
        in order to obtain an estimate of the systematic error and associated
        uncertainty. This is often referred to as the "error budget"

        The values are R_sample / R_nominal, meaning they are a multiplicative
        correction factor to the calibrated data in order to obtain the "true"
        response

        Parameters
        ----------
        gpstime : int
            GPS time
        frequencies : `float`, array-like
            array of frequencies to compute the response
        trials : `int`, optional
            number of times to sample the response
        data : `gwpy.timeseries.TimeSeriesDict` object, optional
            This is the time series data of the TDCF channels (nominal values
            and uncertainty) computed either in the CAL-CS, GDS, or DCS
            pipeline. If this is not provided, or it does not match the GPS
            time and duration, then it will be queried. A LIGO.ORG credential
            will be required
        shift_sample_tf : `complex`, array-like, optional
            Multiply sampled responses by a transfer function. The transfer
            function needs to be computed from the same frequenices as this
            method uses otherwise results are unpredictable
        save_to_file_h5 : `str`, optional
            Path to file for saving response curves and samples as
            HDF5 (.h5 or .hdf5)
        save_to_file_txt : `str`, optional
            Path to file for saving uncertainty envelope as ASCII (.txt)
        seed: `int`, optional
            Seed for the random generation of the uncertainty envelope samples.
            The default value (None) will mean results are not reproducible,
            whereas an integer value will return reproducible results.
        **kwargs
            keyword arguments to pass to sample_response method;
            ex.: supplemental_sensing_gpr for an additional GPR to apply to
            sensing samples

        Returns
        -------
        response_samples : list of `complex128`, array-like
            list of response transfer function samples
        """

        np.random.seed(seed)

        # Precompute the suspension filters at particularly relevant frequencies
        sensing_line_freq = self.darm.calcs.cal_line_sens_pcal_frequency
        _ = self.darm.compute_response_function(frequencies)

        # Only precompute if the section is provided in the model file and any
        # of the values in the output matrix are non-zero
        output_matrix = self.darm.actuation.darm_output_matrix_values()
        if 'actuation_x_arm' in self._config and np.any(output_matrix[0, :]):
            _ = self.darm.actuation.xarm.sus_digital_filters_response(frequencies)
            _ = self.darm.actuation.xarm.sus_digital_filters_response(sensing_line_freq)
        if 'actuation_y_arm' in self._config and np.any(output_matrix[1, :]):
            _ = self.darm.actuation.yarm.sus_digital_filters_response(frequencies)
            _ = self.darm.actuation.yarm.sus_digital_filters_response(sensing_line_freq)

        supplemental_sensing_gpr = kwargs.pop('supplemental_sensing_gpr', None)

        # Sample all the responses
        (response_samples, data, sensing_pars_samples, act_pars_samples, sensing_syserr_samples,
            act_syserr_samples) = self.sample_response(
                gpstime, frequencies, n_trials=trials, data=data,
                supplemental_sensing_gpr=supplemental_sensing_gpr)

        nominal_response, data = self.nominal_response(gpstime, frequencies, data)
        response_samples /= nominal_response

        # Multiply in response curves from previous measurements
        if self.response_curve_file and self.response_curve_file != "":
            for n in range(trials):
                response_samples[n] *= np.interp(
                    frequencies,
                    self.previous_model_response_frequencies,
                    self.previous_model_response_curves[n],
                )

        if shift_sample_tf is not None:
            assert len(frequencies) == len(shift_sample_tf)
            response_samples *= shift_sample_tf

        # Save the draws to a file if requested
        if (save_to_file_h5 is not None):
            if ('.h5' in os.path.splitext(save_to_file_h5) or
                    '.hdf5' in os.path.splitext(save_to_file_h5)):
                save_to_file_h5 = os.path.normpath(save_to_file_h5)
                with h5py.File(save_to_file_h5, 'w') as f:
                    f.create_dataset('config', data=json.dumps(dict(self._config._sections)))
                    f.create_dataset('deltaR/freq', data=frequencies)
                    f.create_dataset('deltaR/draws', data=response_samples)
                    f.create_dataset('CalParams/sensing', data=sensing_pars_samples)
                    f.create_dataset('GPR/sensing', data=sensing_syserr_samples)
                    for i, arm in enumerate(act_pars_samples.keys()):
                        for j, stage in enumerate(act_pars_samples[arm].keys()):
                            f.create_dataset(f'CalParams/{arm}/{stage}',
                                             data=act_pars_samples[arm][stage])
                    for i, arm in enumerate(act_syserr_samples.keys()):
                        for j, stage in enumerate(act_syserr_samples[arm].keys()):
                            f.create_dataset(f'GPR/{arm}/{stage}',
                                             data=act_syserr_samples[arm][stage])
                    if shift_sample_tf:
                        f.create_dataset('shift_sample_tf', data=shift_sample_tf)
                    else:
                        f.create_dataset('shift_sample_tf', data='None')
        if save_to_file_txt is not None:
            response_mag_quant, response_pha_quant = \
                self.response_quantiles(response_samples)
            save_samples_to_txt(save_to_file_txt, frequencies,
                                response_mag_quant, response_pha_quant)

        return response_samples

    def response_uncertainty_combine_with_mon_line_data(self,
                                                        freq,
                                                        response_unc_mag,
                                                        response_unc_phase,
                                                        monitor_line_data,
                                                        output_dir_diagnostics='.',
                                                        save_to_file_txt=None,
                                                        save_GP_models=False,
                                                        seed=None):
        """
        Combine monitor lines to modelled response uncertainty

        This method combines samples from the modelled response uncertainty
        to the monitoring line response measurements via a single GPR, to
        generate a more informed fit.

        Parameters
        ----------
        freq: `float` array-like
            frequencies used for modelling the response uncertainty,
            these must correspond to the values of response_unc_mag, response_unc_phase
        response_mag_quant : `float`, array-like
            2-d array of length(quantiles) x length(response_samples) giving
            magnitude quantiles
        response_pha_quant : `float`, array-like
            2-d array of length(quantiles) x length(response_samples) giving
            phase quantiles in radians
        monitor_line_data : dict
            dictionary of monitoring line data taken ~30min
            before and after the reference time of the modelled
            response. The dictionary must contain keys:
            {'oscillator_frequency', 'TF_mag', 'TF_phase'} with
            values being `float`, array-like for each
        output_dir_diagnostics: `str`, default '.'
            Output directory (path) where the GPR training logging plots will be saved.
        save_to_file_txt : `str`, optional
            Path to file for saving uncertainty envelope as ASCII (.txt)
        save_GP_models : bool, default False
            If True, the GPR TensorFlow checkpointed model will be saved in a
            folder names gp_model_mag/ or gp_model_phase.
            See https://www.tensorflow.org/guide/checkpoint
        seed: `int`, optional
            Seed for the random generation of the uncertainty envelope samples.
            The default value (None) will mean results are not reproducible,
            whereas an integer value will return reproducible results.

        Returns
        -------
        response_unc_mon_mag : `float`, array-like
            2-d array of length(3) x length(response_samples) giving
            magnitude quantiles (16th, 50th, 84th)
        response_unc_mon_phase : `float`, array-like
            2-d array of length(3) x length(response_samples) giving
            phase quantiles (16th, 50th, 84th)

        """
        from .regression_utils import create_GP_model, train_GP_parameters

        np.random.seed(seed)

        # The number of monitoring measurements per freq determines how many
        # points (`ndraws`) to generate from the PyDarm model, such that the
        # envelope is well representative of the data given our model.
        Nmeas_per_freq = np.max(
            [
                monitor_line_data[
                    monitor_line_data["oscillator_frequency"] == freq
                ].shape[0]
                for freq in monitor_line_data["oscillator_frequency"].unique()
            ]
        )
        # If few monitoring meas, don't calculate `ndraws` as likely too small.
        # Here `ndraws` was manually chosen based on how many points are required
        # to fit an O4a envelope and it matching the PyDarm model.
        if int(Nmeas_per_freq) < 22:
            ndraws = 10
        else:
            ndraws = int(Nmeas_per_freq/3)
        # Generating "Gaussian samples" of the PyDarm model
        frequencies = []
        y_mag_draws = []
        y_phase_draws = []
        for i, ff in enumerate(freq):
            for point in np.random.normal(
                loc=np.array(response_unc_mag[1][freq == ff] - 1) * 100,
                scale=((np.array(response_unc_mag[2][freq == ff] - 1) * 100)
                       - (np.array(response_unc_mag[1][freq == ff] - 1) * 100)),
                    size=ndraws):
                frequencies.append(freq[i])
                y_mag_draws.append(point)

        for i, ff in enumerate(freq):
            for point in np.random.normal(
                loc=np.degrees(np.array(response_unc_phase[1][freq == ff])),
                scale=(np.degrees(np.array(response_unc_phase[2][freq == ff]))
                       - np.degrees(np.array(response_unc_phase[1][freq == ff]))),
                    size=ndraws):
                y_phase_draws.append(point)
        data = {
            "oscillator_frequency": frequencies,
            "TF_phase": y_phase_draws,
            "TF_mag": y_mag_draws,
        }

        # Combine monitoring data and model samples together
        mon_data = (
            monitor_line_data.copy()
        )  # copy data-set in order to not modify in place the original
        mon_data["TF_mag"] = (mon_data["TF_mag"].values - 1) * 100

        # Combining sweep_draws and mon_data by making lists of dictionaries
        sweep_draws = [
            {"oscillator_frequency": freq, "TF_phase": phase, "TF_mag": mag}
            for freq, phase, mag in zip(data["oscillator_frequency"],
                                        data["TF_phase"],
                                        data["TF_mag"])
        ]
        mon_data = mon_data.to_dict(orient='records')
        combined_list = mon_data + sweep_draws
        combined_list.sort(key=lambda x: x["oscillator_frequency"])
        df_sweep = {key: [dic[key] for dic in combined_list] for key in combined_list[0]}

        # Main Computation Loop
        response_unc_mon = {}
        for meas in ["mag", "phase"]:
            X = np.log(np.array(df_sweep["oscillator_frequency"])).reshape(-1, 1)
            Y = np.array(df_sweep[f"TF_{meas}"]).reshape(-1, 1)
            if output_dir_diagnostics != '.':
                if not os.path.exists(f"{output_dir_diagnostics}/diagnostics_plots"):
                    os.makedirs(f"{output_dir_diagnostics}/diagnostics_plots")
                with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "w") as f:  # noqa E501
                    f.write(f"Data shapes X:{X.shape}, Y:{Y.shape} \n")
                    f.close()
            model = create_GP_model(X)
            best_epoch = train_GP_parameters(X, Y, model, meas, output_dir_diagnostics)

            if best_epoch < 4:  # Edge case, possible numerical instabilities in loss function
                if output_dir_diagnostics != '.':
                    with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "a") as f:  # noqa E501
                        f.write("Training was suspiciously short, adjusting optimiser's hyper-parameters and restarting..\n")  # noqa E501
                        f.close()
                # Depending on the diagnosis of the error you can vary:
                # `patience`, `epochs`, `initial_lr`, `gamma` or `jitter`
                # Please adjust this accordingly if issues arise - current based on O4a by VdE
                model = create_GP_model(X)  # This resets the loss function
                _ = train_GP_parameters(X, Y, model, meas, output_dir_diagnostics, gamma=0.05, jitter=1e-3)  # noqa E501

            if save_GP_models is False:  # if True the TF checkpointed model objects will be saved
                shutil.rmtree(f'{output_dir_diagnostics}/gp_model_{meas}')
            Xpred = np.log(freq).reshape(-1, 1)
            Ymean, Yvar = model.predict_y(Xpred)
            y_pred = Ymean.numpy().squeeze()
            sigma_gp = np.sqrt(Yvar.numpy().squeeze())
            # Compute uncertainty in quadrature
            if meas == "mag":

                def output_units(x):
                    return (x / 100) + 1

            else:

                def output_units(x):
                    return np.deg2rad(x)

            gp_16th_pp = np.array(output_units(y_pred - sigma_gp))
            gp_84th_pp = np.array(output_units(y_pred + sigma_gp))
            gp_median = np.array(output_units(y_pred))
            response_unc_mon[meas] = np.vstack((gp_16th_pp, gp_median, gp_84th_pp))
        if save_to_file_txt is not None:
            save_samples_to_txt(save_to_file_txt, freq,
                                response_unc_mon['mag'], response_unc_mon['phase'])
        return response_unc_mon['mag'], response_unc_mon['phase']

    @staticmethod
    def response_quantiles(response_samples, quantiles=(16, 50, 84)):
        """
        Calculate the quantiles of response uncertainty samples

        Parameters
        ----------
        response_samples : `complex128`, list
            list of arrays of ration of sampled responses to nominal response
        quantiles : `float`, list, optional
            list of quantiles desired to be computed

        Returns
        -------
        response_mag_quant : `float`, array-like
            2-d array of length(quantiles) x length(response_samples) giving
            magnitude quantiles
        response_pha_quant : `float`, array-like
            2-d array of length(quantiles) x length(response_samples) giving
            phase quantiles in radians
        """
        # Set up arrays
        response_mag_quant = np.zeros((len(quantiles), len(response_samples[0])))
        response_pha_quant = np.zeros((len(quantiles), len(response_samples[0])))

        # Calculate the quantiles requested
        for i in range(len(quantiles)):
            response_mag_quant[i, :] = np.percentile(
                np.abs(response_samples), quantiles[i], axis=0)
            response_pha_quant[i, :] = np.percentile(
                np.angle(response_samples), quantiles[i], axis=0)

        return response_mag_quant, response_pha_quant

    @staticmethod
    def plot_response_samples(frequencies, response_mag_quant,
                              response_pha_quant, ifo,
                              y_mag=10, y_pha=10, filename=None,
                              monitor_line_data=None):
        """
        Parameters
        ----------
        frequencies : `float`, array-like
        response_mag_quant : `float`, array-like
        response_pha_quant : `float`, array-like
        ifo : `str`, H1 or L1
        y_mag : `float`, optional
            Y-axis magnitude range, in percent (default is +/- 10%)
        y_pha : `float`, optional
            Y-axis phase range, in degree (default is +/- 10 degrees)
        monitor_line_data : dict
            dictionary of monitoring line data taken ~30min
            before and after the reference time of the modelled
            response. The dictionary must contain keys:
            {'oscillator_frequency', 'TF_mag', 'TF_phase'} with
            values being `float`, array-like for each

        Returns
        -------
        fig: `matplotlib.figure.Figure`, figure of uncertainty
        """
        import matplotlib as mpl
        mpl.rcParams.update({'text.usetex': False,
                             'axes.linewidth': 1,
                             'axes.grid': True,
                             'axes.labelweight': 'normal',
                             'font.family': 'DejaVu Sans',
                             'font.size': 20})
        if ifo == 'H1':
            ifo_color = 'r'
        else:
            ifo_color = 'b'

        freqRange = [10.0, 5000.0]
        yMagRange = [-y_mag, y_mag]
        yPhaseRange = [-y_pha, y_pha]

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 12))
        ax0, ax1 = axes.flat

        ax0.plot(frequencies, 100 * (response_mag_quant[1, :] - 1.0),
                 color=ifo_color, label=r'Median')
        ax0.plot(frequencies, 100 * (response_mag_quant[0, :] - 1.0),
                 linestyle='--', color=ifo_color, label=r'$1 \sigma$ Uncertainty')
        ax0.plot(frequencies, 100 * (response_mag_quant[2, :] - 1.0),
                 linestyle='--', color=ifo_color)
        ax0.fill_between(frequencies, 100 * (response_mag_quant[0, :] - 1.0),
                         100 * (response_mag_quant[2, :] - 1.0), color=ifo_color, alpha=0.3)
        ax0.set_xlim(freqRange)
        ax0.set_ylim(yMagRange)
        ax0.minorticks_on()
        ax0.set_yticks(np.arange(yMagRange[0]+(yMagRange[0] % 2), yMagRange[1]+1, 2))
        ax0.grid(ls='-', which='major', lw=1.1)
        ax0.grid(ls='--', which='minor')

        ax1.plot(frequencies, 180/np.pi*response_pha_quant[1, :], color=ifo_color, label=r'Median')
        ax1.plot(frequencies, 180/np.pi*response_pha_quant[0, :], linestyle='--',
                 color=ifo_color, label=r'$1 \sigma$ Uncertainty')
        ax1.plot(frequencies, 180/np.pi*response_pha_quant[2, :], linestyle='--', color=ifo_color)
        ax1.fill_between(frequencies, 180/np.pi*response_pha_quant[0, :],
                         180/np.pi*response_pha_quant[2, :], color=ifo_color, alpha=0.3)
        if monitor_line_data is not None:
            monitor_lines_frequencies = monitor_line_data['oscillator_frequency'].unique().tolist()
            monitor_lines_frequencies.sort()
            for freqnum in monitor_lines_frequencies:
                monitor_mag_single = 100*(monitor_line_data[monitor_line_data['oscillator_frequency'] == freqnum]['TF_mag'].values-1)  # noqa E501
                monitor_phase_single = monitor_line_data[monitor_line_data['oscillator_frequency'] == freqnum]['TF_phase'].values  # noqa E501
                ax0.plot(
                    float(freqnum)*np.ones_like(monitor_mag_single),
                    monitor_mag_single, '.', color='k', alpha=0.2)
                ax1.plot(
                    float(freqnum)*np.ones_like(monitor_phase_single),
                    monitor_phase_single, '.', color='k', alpha=0.2)

            ax_twin0 = ax0.twiny()
            ax_twin0.set_xticks(np.log10(monitor_lines_frequencies))
            ax_twin0.set_xticklabels(np.around(monitor_lines_frequencies, decimals=1), fontsize=12)
            ax_twin0.set_xlim([np.log10(freqRange[0]), np.log10(freqRange[1])])
            ax_twin0.grid(linestyle='dashed', color='black')

            ax_twin1 = ax1.twiny()
            ax_twin1.set_xticks(np.log10(monitor_lines_frequencies))
            ax_twin1.set_xticklabels([])
            ax_twin1.set_xlim([np.log10(freqRange[0]), np.log10(freqRange[1])])
            ax_twin1.grid(linestyle='dashed', color='black')

        ax1.set_xlim(freqRange)
        ax1.set_ylim(yPhaseRange)
        ax1.minorticks_on()
        ax1.set_yticks(np.arange(yPhaseRange[0]+(yPhaseRange[0] % 2), yPhaseRange[1]+1, 2))
        ax1.grid(ls='-', which='major', lw=1.1)
        ax1.grid(ls='--', which='minor')

        for ax in axes.flat:
            ax.set_xscale("log")
            ax.set_xticks(np.array([20, 50, 100, 200, 500, 1000, 2000, 5000]))
            ax.set_xticklabels(['20', '50', '100', '200', '500', '1000', '2000', '5000'])
            legend = ax.legend(loc='lower center', ncol=2, handlelength=3)
            for i in legend.get_lines():
                i.set_linewidth(2)

        ax1.set_xlabel(r'Frequency [Hz]')
        ax0.set_ylabel(r'$|R^{\rm (sample)}/R^{\rm (MAP)}|-1$ [%]')
        ax1.set_ylabel(r'$\angle[R^{\rm (sample)}/R^{\rm (MAP)}]$ [deg]')
        if filename is not None:
            fig.savefig(filename, bbox_inches='tight', pad_inches=0.2)

        return fig

    @staticmethod
    def plot_response_samples_compare(frequencies, RRMag, RRPha,
                                      response_mag_quants, response_pha_quants, ifo,
                                      y_mag=10, y_pha=10, filename=None,
                                      monitor_line_data=None):
        import matplotlib as mpl
        mpl.rcParams.update({'text.usetex': False,
                             'axes.linewidth': 1,
                             'axes.grid': True,
                             'axes.labelweight': 'normal',
                             'font.family': 'DejaVu Sans',
                             'font.size': 20})
        if ifo == 'H1':
            ifo_color = ['r', 'gray']
        else:
            ifo_color = ['b', 'gray']

        label = {0: r'GPflow Median', 1: r'Pydarm Median'}
        freqRange = [10.0, 5000.0]
        yMagRange = [-y_mag, y_mag]
        yPhaseRange = [-y_pha, y_pha]

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 12))
        ax0, ax1 = axes.flat
        for i, response_mag_quant in enumerate(response_mag_quants):
            ax0.plot(frequencies, 100 * (response_mag_quant[1, :] - 1.0),
                     color=ifo_color[i], label=label[i])
            ax0.plot(frequencies, 100 * (response_mag_quant[0, :] - 1.0),
                     linestyle='--', color=ifo_color[i], label=r'$1 \sigma$ Uncertainty')
            ax0.plot(frequencies, 100 * (response_mag_quant[2, :] - 1.0),
                     linestyle='--', color=ifo_color[i])
            ax0.fill_between(frequencies, 100 * (response_mag_quant[0, :] - 1.0),
                             100 * (response_mag_quant[2, :] - 1.0), color=ifo_color[i], alpha=0.3)
        ax0.set_xlim(freqRange)
        ax0.set_ylim(yMagRange)
        ax0.minorticks_on()
        ax0.set_yticks(np.arange(yMagRange[0]+(yMagRange[0] % 2), yMagRange[1]+1, 2))
        ax0.grid(ls='-', which='major', lw=1.1)
        ax0.grid(ls='--', which='minor')

        for i, response_pha_quant in enumerate(response_pha_quants):
            ax1.plot(frequencies, 180/np.pi*response_pha_quant[1, :], color=ifo_color[i], label=label[i])  # noqa E501
            ax1.plot(frequencies, 180/np.pi*response_pha_quant[0, :], linestyle='--',
                     color=ifo_color[i], label=r'$1 \sigma$ Uncertainty')
            ax1.plot(frequencies, 180/np.pi*response_pha_quant[2, :], linestyle='--', color=ifo_color[i])  # noqa E501
            ax1.fill_between(frequencies, 180/np.pi*response_pha_quant[0, :],
                             180/np.pi*response_pha_quant[2, :], color=ifo_color[i], alpha=0.3)
        if monitor_line_data is not None:
            monitor_lines_frequencies = monitor_line_data['oscillator_frequency'].unique().tolist()
            monitor_lines_frequencies.sort()
            for freqnum in monitor_lines_frequencies:
                monitor_mag_single = 100*(monitor_line_data[monitor_line_data['oscillator_frequency'] == freqnum]['TF_mag'].values-1)  # noqa E501
                monitor_phase_single = monitor_line_data[monitor_line_data['oscillator_frequency'] == freqnum]['TF_phase'].values  # noqa E501
                ax0.plot(
                    float(freqnum)*np.ones_like(monitor_mag_single),
                    monitor_mag_single, '.', color='k', alpha=0.2)
                ax1.plot(
                    float(freqnum)*np.ones_like(monitor_phase_single),
                    monitor_phase_single, '.', color='k', alpha=0.2)

            ax_twin0 = ax0.twiny()
            ax_twin0.set_xticks(np.log10(monitor_lines_frequencies))
            ax_twin0.set_xticklabels(np.around(monitor_lines_frequencies, decimals=1), fontsize=12)
            ax_twin0.set_xlim([np.log10(freqRange[0]), np.log10(freqRange[1])])
            ax_twin0.grid(linestyle='dashed', color='black')

            ax_twin1 = ax1.twiny()
            ax_twin1.set_xticks(np.log10(monitor_lines_frequencies))
            ax_twin1.set_xticklabels([])
            ax_twin1.set_xlim([np.log10(freqRange[0]), np.log10(freqRange[1])])
            ax_twin1.grid(linestyle='dashed', color='black')

        ax1.set_xlim(freqRange)
        ax1.set_ylim(yPhaseRange)
        ax1.minorticks_on()
        ax1.set_yticks(np.arange(yPhaseRange[0]+(yPhaseRange[0] % 2), yPhaseRange[1]+1, 2))
        ax1.grid(ls='-', which='major', lw=1.1)
        ax1.grid(ls='--', which='minor')

        for ax in axes.flat:
            ax.set_xscale("log")
            ax.set_xticks(np.array([20, 50, 100, 200, 500, 1000, 2000, 5000]))
            ax.set_xticklabels(['20', '50', '100', '200', '500', '1000', '2000', '5000'])
            legend = ax.legend(loc='lower center', ncol=2, handlelength=3)
            for i in legend.get_lines():
                i.set_linewidth(2)

        ax1.set_xlabel(r'Frequency [Hz]')
        ax0.set_ylabel(r'$|R^{\rm (sample)}/R^{\rm (MAP)}|-1$ [%]')
        ax1.set_ylabel(r'$\angle[R^{\rm (sample)}/R^{\rm (MAP)}]$ [deg]')
        if filename is not None:
            fig.savefig(filename, bbox_inches='tight', pad_inches=0.2)

        return fig
