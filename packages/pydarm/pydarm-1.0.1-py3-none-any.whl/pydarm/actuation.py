# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.

import numpy as np

from scipy import signal, io

from .utils import digital_delay_filter
from .utils import compute_digital_filter_response, freqrespZPK
from .model import Model


class ActuationModel(Model):
    """
    An arm actuation model object

    This is a class to set up the model for the actuation function from a
    configuration file with all the information about where the data is stored

    """

    def __init__(self, config, measurement):
        super().__init__(config, measurement=measurement)

        # TODO need some way of validating the configuration file is
        # appropriate

        # Set default delay values if not set
        if (not hasattr(self, 'unknown_actuation_delay') or
                self.unknown_actuation_delay == ''):
            self.unknown_actuation_delay = 0
        if not hasattr(self, 'uim_delay') or self.uim_delay == '':
            self.uim_delay = 0
        if not hasattr(self, 'pum_delay') or self.pum_delay == '':
            self.pum_delay = 0
        if not hasattr(self, 'tst_delay') or self.tst_delay == '':
            self.tst_delay = 0

        # Setting up to the list to save loading in the suspension filters
        self.tst_digital_filter_response_list = []
        self.pum_digital_filter_response_list = []
        self.uim_digital_filter_response_list = []
        self.filter_response_freq_list = []

        self.tst_drivealign_to_displacement_list = []
        self.pum_drivealign_to_displacement_list = []
        self.uim_drivealign_to_displacement_list = []
        self.drivealign_to_displacement_freq_list = []

    def analog_driver_response(self, frequencies):
        """
        The transfer function of the analog driver electronics. By default,
        the output will be a dictionary for UIM, PUM, and TST with
        dictionaries for each containing the quadrants UL, LL, UR, LR.
        Transfer functions are unity with zero phase unless the params
        file/string contains a <uim|pum|tst>_driver_meas_<z|p>_<ul|ll|ur|lr>
        for the particular quadrant and values

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        out : dict, `complex128`, array-like
            transfer function response of the uncompensated driver electronics

        """

        out = {'UIM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'PUM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'TST': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')}}

        for i, stage in enumerate(out.keys()):
            for j, quadrant in enumerate(out[stage].keys()):

                # Emit error if trying to use the old format
                if ((hasattr(self, f'{stage.lower()}_driver_meas_z_'
                                   f'{quadrant.lower()}') and
                     not hasattr(self, f'{stage.lower()}_driver_uncompensated_'
                                       f'z_{quadrant.lower()}')) or
                    (hasattr(self, f'{stage.lower()}_driver_meas_p_'
                                   f'{quadrant.lower()}') and
                     not hasattr(self, f'{stage.lower()}_driver_uncompensated_'
                                       f'p_{quadrant.lower()}'))):
                    raise KeyError(
                        'Using old format for zeros and poles. Please check'
                        ' your configuration string/file and use the'
                        ' updated format to specify'
                        ' compensated/uncompensated parameters. '
                        f'Stage: {stage.lower()}, Quadrant: {quadrant.lower()}')

                # Start with empty lists for zeros and poles. Extend as needed
                zeros = []
                poles = []
                if (hasattr(self, f'{stage.lower()}_driver_uncompensated_z_'
                                  f'{quadrant.lower()}') and
                        hasattr(self, f'{stage.lower()}_driver_uncompensated_'
                                      f'p_{quadrant.lower()}')):
                    zeros.extend(getattr(
                        self, f'{stage.lower()}_driver_uncompensated_z_'
                              f'{quadrant.lower()}'))
                    poles.extend(getattr(
                        self, f'{stage.lower()}_driver_uncompensated_p_'
                              f'{quadrant.lower()}'))
                if (hasattr(self, f'{stage.lower()}_driver_compensated_z_'
                                  f'{quadrant.lower()}') and
                        getattr(self, f'{stage.lower()}_front_end_driver_'
                                      f'compensation_{quadrant.lower()}') == 'OFF'):
                    zeros.extend(getattr(self, f'{stage.lower()}_driver_'
                                               f'compensated_z_{quadrant.lower()}'))
                if (hasattr(self, f'{stage.lower()}_driver_compensated_p_'
                                  f'{quadrant.lower()}') and
                        getattr(self, f'{stage.lower()}_front_end_driver_'
                                      f'compensation_{quadrant.lower()}') == 'OFF'):
                    poles.extend(getattr(self, f'{stage.lower()}_driver_'
                                               f'compensated_p_{quadrant.lower()}'))

                # Convert lists to numpy arrays
                zeros = np.asarray(zeros)
                poles = np.asarray(poles)

                # Gain is the ratio of poles / zeros
                # NB: if both are empty, then this returns a gain of 1.0
                gain = np.prod(2.0*np.pi*poles) / np.prod(2.0*np.pi*zeros)

                # LTI model
                model = signal.ZerosPolesGain(
                    -2.0*np.pi*zeros,
                    -2.0*np.pi*poles,
                    gain)

                # The frequency response of the LTI model saved to
                # out[stage][quadrant]
                tf = signal.freqresp(model, 2.0*np.pi*frequencies)[1]
                out[stage][quadrant] = tf

        return out

    def uim_dc_gain_Apct(self):
        """This computes the UIM DC gain in units of amps / count

        """

        return 4 * 0.25 * self.dac_gain * self.uim_driver_dc_trans_apv

    def pum_dc_gain_Apct(self):
        """This computes the PUM DC gain in units of amps / count

        """

        return 4 * 0.25 * self.dac_gain * self.pum_driver_dc_trans_apv * \
            self.pum_coil_outf_signflip

    def tst_dc_gain_V2pct(self):
        """This computes the TST DC gain in units of volts**2 / count

        """

        return 4 * 0.25 * self.dac_gain * self.tst_driver_dc_gain_vpv_lv * \
            2 * self.tst_driver_dc_gain_vpv_hv * \
            self.actuation_esd_bias_voltage

    def uim_dc_gain_Npct(self):
        """This computes the UIM DC gain in units of Newtons / count

        """

        return self.uim_dc_gain_Apct() * self.uim_npa

    def pum_dc_gain_Npct(self):
        """
        This computes the PUM DC gain in units of Newtons / count
        """

        return self.pum_dc_gain_Apct() * self.pum_npa

    def tst_dc_gain_Npct(self):
        """This computes the TST DC gain in units of Newtons / count

        """

        return self.tst_dc_gain_V2pct() * self.tst_npv2

    def sus_digital_filters(self, frequencies):
        """
        The transfer function of the SUS digital filters

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tst_isc_inf_filter_response : `complex128`, array-like
            transfer function response of the ISC_INF digital filters in the
            TST path
        tst_lock_filter_response : `complex128`, array-like
            transfer function response of the LOCK digital filters in the
            TST path
        tst_drive_align_filter_response : `complex128`, array-like
            transfer function response of the DRIVEALIGN digital filters in
            the TST path
        pum_lock_filter_response : `complex128`, array-like
            transfer function response of the LOCK digital filters in the
            PUM path
        pum_drive_align_filter_response : `complex128`, array-like
            transfer function response of the DRIVEALIGN digital filters in the
             PUM path
        uim_lock_filter_response : `complex128`, array-like
            transfer function response of the LOCK digital filters in the UIM
            path
        uim_drive_align_filter_response : `complex128`, array-like
            transfer function response of the DRIVEALIGN digital filters in the
            UIM path

        """

        # Start with TST stage filters
        tst_isc_inf_filter_response, pfilt = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_isc_inf_bank, self.tst_isc_inf_modules[0],
                self.tst_isc_inf_gain, frequencies)
        tst_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_lock_bank, self.tst_lock_modules[0],
                self.tst_lock_gain, frequencies, pfilt)[0]
        tst_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_drive_align_bank, self.tst_drive_align_modules[0],
                self.tst_drive_align_gain, frequencies, pfilt)[0]

        # The PUM stage feedback is to the same SUS as TST stage, so
        # we can reuse the pfilt variable from above
        pum_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_lock_bank, self.pum_lock_modules[0],
                self.pum_lock_gain, frequencies, pfilt)[0]
        pum_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_drive_align_bank, self.pum_drive_align_modules[0],
                self.pum_drive_align_gain, frequencies, pfilt)[0]

        # The UIM stage feedback is to the same SUS as PUM stage, so
        # we can reuse the pfilt variable from above
        uim_lock_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_lock_bank, self.uim_lock_modules[0],
                self.uim_lock_gain, frequencies, pfilt)[0]
        uim_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_drive_align_bank, self.uim_drive_align_modules[0],
                self.uim_drive_align_gain, frequencies, pfilt)[0]

        return tst_isc_inf_filter_response, tst_lock_filter_response, \
            tst_drive_align_filter_response, pum_lock_filter_response, \
            pum_drive_align_filter_response, uim_lock_filter_response, \
            uim_drive_align_filter_response

    def sus_digital_filters_response(self, frequencies):
        """
        The transfer function of the SUS digital filters

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the UIM path
        pum_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the PUM path
        tst_digital_filter_response : `complex128`, array-like
            transfer function response of the digital filters in the TST path

        """

        use_index = False
        idx = 0
        for i, saved_freq_array in enumerate(self.filter_response_freq_list):
            if np.array_equiv(np.atleast_1d(frequencies),
                              np.atleast_1d(saved_freq_array)):
                idx = i
                use_index = True
                break

        if use_index:
            tst_digital_filter_response = np.copy(self.tst_digital_filter_response_list[idx])
            pum_digital_filter_response = np.copy(self.pum_digital_filter_response_list[idx])
            uim_digital_filter_response = np.copy(self.uim_digital_filter_response_list[idx])

        else:
            tst_isc_inf_filter_response, tst_lock_filter_response, \
                tst_drive_align_filter_response, pum_lock_filter_response, \
                pum_drive_align_filter_response, uim_lock_filter_response, \
                uim_drive_align_filter_response = \
                self.sus_digital_filters(frequencies)

            # Start with TST stage filters
            tst_digital_filter_response = tst_isc_inf_filter_response * \
                tst_lock_filter_response * tst_drive_align_filter_response

            pum_digital_filter_response = tst_isc_inf_filter_response * \
                tst_lock_filter_response * pum_lock_filter_response * \
                pum_drive_align_filter_response

            uim_digital_filter_response = tst_isc_inf_filter_response * \
                tst_lock_filter_response * pum_lock_filter_response * \
                uim_lock_filter_response * uim_drive_align_filter_response

            self.filter_response_freq_list.append(frequencies)
            self.tst_digital_filter_response_list.append(tst_digital_filter_response)
            self.pum_digital_filter_response_list.append(pum_digital_filter_response)
            self.uim_digital_filter_response_list.append(uim_digital_filter_response)

        return uim_digital_filter_response, \
            pum_digital_filter_response, \
            tst_digital_filter_response

    def sus_digital_compensation_response(self, frequencies):
        """
        The transfer function of the SUS compensation filters for driver
        electronics. By default, the output will be a dictionary for UIM,
        PUM, and TST with dictionaries for each containing the quadrants
        UL, LL, UR, LR. Transfer functions are unity with zero phase unless
        the params file/string contains:
        <uim|pum|tst>_compensation_filter_bank_<ul|ll|ur|lr> with a name;
        <uim|pum|tst>_compensation_filter_modules_in_use_<ul|ll|ur|lr> with
        list of modules turned on; and
        <uim|pum|tst>_compensation_filter_gain_<ul|ll|ur|lr>

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        out : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant

        """

        out = {'UIM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'PUM': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')},
               'TST': {'UL': np.ones(len(frequencies), dtype='complex128'),
                       'LL': np.ones(len(frequencies), dtype='complex128'),
                       'UR': np.ones(len(frequencies), dtype='complex128'),
                       'LR': np.ones(len(frequencies), dtype='complex128')}}

        pfilt = None
        for i, stage in enumerate(out.keys()):
            for j, quadrant in enumerate(out[stage].keys()):

                # Emit error if trying to use the old format
                if ((hasattr(self, f'{stage.lower()}_compensation_filter_bank_'
                                   f'{quadrant.lower()}') and
                     not hasattr(self, f'{stage.lower()}_filter_bank_'
                                       f'{quadrant.lower()}')) or
                    (hasattr(self, f'{stage.lower()}_compensation_filter_'
                                   f'modules_in_use_{quadrant.lower()}') and
                     not hasattr(self, f'{stage.lower()}_compensation_filter_'
                                       f'modules_{quadrant.lower()}')) or
                    (hasattr(self, f'{stage.lower()}_compensation_filter_gain_'
                                   f'{quadrant.lower()}') and
                     not hasattr(self, f'{stage.lower()}_filter_gain_{quadrant.lower()}'))):
                    raise KeyError(
                        'Using the old format for driver compensation'
                        ' parameters. Please update your configuration'
                        ' file/string to use the new format.')

                if hasattr(self, f'{stage.lower()}_filter_bank_{quadrant.lower()}'):
                    bank = getattr(self,
                                   f'{stage.lower()}_filter_bank_{quadrant.lower()}')
                if (hasattr(self, f'{stage.lower()}_compensation_filter_'
                                  f'modules_{quadrant.lower()}') and
                        getattr(self, f'{stage.lower()}_front_end_driver_'
                                      f'compensation_{quadrant.lower()}') == 'OFF'):
                    modules = getattr(
                        self,
                        f'{stage.lower()}_compensation_filter_modules_{quadrant.lower()}')
                if hasattr(self, f'{stage.lower()}_filter_gain_{quadrant.lower()}'):
                    gain = getattr(
                        self, f'{stage.lower()}_filter_gain_{quadrant.lower()}')

                if ('bank' in locals() and len(bank) > 0 and
                        'modules' in locals() and 'gain' in locals()):
                    tf, pfilt = compute_digital_filter_response(
                        self.dpath(self.sus_filter_file),
                        bank, modules, gain, frequencies, pfilt)

                    out[stage][quadrant] *= tf
                    del bank, gain, modules

        return out

    def combine_sus_quadrants(self, frequencies):
        """
        Combine the digital and analog paths for the SUS quadrants on a
        per-stage and per-path basis. Meaning
        (0.25 x UIM UL digital x UIM UL analog +
        0.25 x UIM LL digital x UIM LL analog + ...) and so on for each
        stage

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the UIM
        pum : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the PUM
        tst : dict, `complex128`, array-like
            transfer function response of the digital compensation filters in
            each path and quadrant for the TST

        """

        sus_dict_digital = self.sus_digital_compensation_response(frequencies)
        sus_dict_analog = self.analog_driver_response(frequencies)

        uim = 0.25 * (
            sus_dict_digital['UIM']['UL'] * sus_dict_analog['UIM']['UL'] +
            sus_dict_digital['UIM']['LL'] * sus_dict_analog['UIM']['LL'] +
            sus_dict_digital['UIM']['UR'] * sus_dict_analog['UIM']['UR'] +
            sus_dict_digital['UIM']['LR'] * sus_dict_analog['UIM']['LR'])
        pum = 0.25 * (
            sus_dict_digital['PUM']['UL'] * sus_dict_analog['PUM']['UL'] +
            sus_dict_digital['PUM']['LL'] * sus_dict_analog['PUM']['LL'] +
            sus_dict_digital['PUM']['UR'] * sus_dict_analog['PUM']['UR'] +
            sus_dict_digital['PUM']['LR'] * sus_dict_analog['PUM']['LR'])
        tst = 0.25 * (
            sus_dict_digital['TST']['UL'] * sus_dict_analog['TST']['UL'] +
            sus_dict_digital['TST']['LL'] * sus_dict_analog['TST']['LL'] +
            sus_dict_digital['TST']['UR'] * sus_dict_analog['TST']['UR'] +
            sus_dict_digital['TST']['LR'] * sus_dict_analog['TST']['LR'])

        return uim, pum, tst

    def actuation_stage_residual(self, frequencies, stage='TST'):
        """
        This is the actuation residual for a given stage on a given arm (this
        object), meaning it contains everything in the actuation except for
        the output matrix, the digital distribution filters, the actuator
        gain, and suspension dynamics.

        See T1900169

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        stage : `str`, optional
            UIM, PUM or TST (default = 'TST')

        Returns
        -------
        A_mn_res : `complex128`, array-like
            transfer function response of the residual actuation function

        """

        # SUS to IOP and IOP to analog digital time delays (see G1601472)
        sus_to_iop_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        iop_to_analog_delay_response = signal.dfreqresp(
            digital_delay_filter(4, 65536), 2.0*np.pi*frequencies/65536)[1]

        # digital anti-imaging filter
        digital_ai_filter_response = \
            self.digital_aa_or_ai_filter_response(frequencies)

        # analog anti-imaging filter response
        analog_ai_filter_response = \
            self.analog_aa_or_ai_filter_response(frequencies)

        # Combine analog driver electronics for each quadrant with the
        # digital compensation for each quadrant (if specified), and
        # then take the mean of the four quadrants for each stage. Most
        # often, this only contains the high frequency response that we
        # cannot compensate.
        # Order: [UIM, PUM, TST]
        stages_tfs = self.combine_sus_quadrants(frequencies)
        stage_index = ['uim', 'pum', 'tst'].index(stage.lower())
        stage_tf = stages_tfs[stage_index]

        # Unknown overall time delay
        unknown_actuation_delay = np.exp(-2.0*np.pi*1j *
                                         self.unknown_actuation_delay *
                                         frequencies)

        # Independent time delay
        delay = getattr(self, f'{stage.lower()}_delay')
        stage_delay = np.exp(-2.0*np.pi*1j*delay*frequencies)

        A_mn_res = (sus_to_iop_delay_response *
                    iop_to_analog_delay_response *
                    digital_ai_filter_response *
                    analog_ai_filter_response *
                    stage_tf *
                    unknown_actuation_delay *
                    stage_delay)

        return A_mn_res

    @staticmethod
    def matlab_force2length_response(suspension_file, frequencies):
        """
        Load the ZPK output from the matlab exported values and output a
        frequency response. This function expects variables in a .mat file to
        be UIMz, UIMp, UIMk, PUMz, PUMp, PUMk, TSTz, TSTp, and TSTk

        Parameters
        ----------
        suspension_file: `str`
            path and filename to .mat file that has the ZPK arrays
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        UIM_F2L_freqresp : `complex128`, array-like
            transfer function response of the UIM stage
        PUM_F2L_freqresp : `complex128`, array-like
            transfer function response of the PUM stage
        TST_F2L_freqresp : `complex128`, array-like
            transfer function response of the TST stage

        """

        mat = io.loadmat(suspension_file)
        UIM_F2L = signal.ZerosPolesGain(mat['UIMz'][:, 0], mat['UIMp'][:, 0],
                                        mat['UIMk'][0, 0])
        PUM_F2L = signal.ZerosPolesGain(mat['PUMz'][:, 0], mat['PUMp'][:, 0],
                                        mat['PUMk'][0, 0])
        TST_F2L = signal.ZerosPolesGain(mat['TSTz'][:, 0], mat['TSTp'][:, 0],
                                        mat['TSTk'][0, 0])
        UIM_F2L_freqresp = freqrespZPK(UIM_F2L, 2.0*np.pi*frequencies)
        PUM_F2L_freqresp = freqrespZPK(PUM_F2L, 2.0*np.pi*frequencies)
        TST_F2L_freqresp = freqrespZPK(TST_F2L, 2.0*np.pi*frequencies)

        return UIM_F2L_freqresp, PUM_F2L_freqresp, TST_F2L_freqresp

    def digital_out_to_displacement(self, frequencies):
        """
        This computes the transfer function from the output of the DRIVEALIGN
        filter bank of each stage to displacement of the test mass

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage
        tst_response : `complex128`, array-like
            transfer function response of the TST stage

        """

        use_index = False
        idx = 0
        for i, saved_freq_array in enumerate(self.drivealign_to_displacement_freq_list):
            if np.array_equiv(np.atleast_1d(frequencies),
                              np.atleast_1d(saved_freq_array)):
                idx = i
                use_index = True
                break

        if use_index:
            tst_response = np.copy(self.tst_drivealign_to_displacement_list[idx])
            pum_response = np.copy(self.pum_drivealign_to_displacement_list[idx])
            uim_response = np.copy(self.uim_drivealign_to_displacement_list[idx])

        else:

            # Analog force to length response for each stage from Matlab
            sus_file = self.dpath(self.suspension_file)
            [uim_f2l_response,
             pum_f2l_response,
             tst_f2l_response] = self.matlab_force2length_response(
                 sus_file, frequencies)

            # Actuation stage residuals
            A_u_res = self.actuation_stage_residual(frequencies, stage='UIM')
            A_p_res = self.actuation_stage_residual(frequencies, stage='PUM')
            A_t_res = self.actuation_stage_residual(frequencies, stage='TST')

            # Everything together now!
            tst_response = (A_t_res *
                            self.tst_dc_gain_Npct() *
                            tst_f2l_response)
            pum_response = (A_p_res *
                            self.pum_dc_gain_Npct() *
                            pum_f2l_response)
            uim_response = (A_u_res *
                            self.uim_dc_gain_Npct() *
                            uim_f2l_response)

            self.drivealign_to_displacement_freq_list.append(frequencies)
            self.tst_drivealign_to_displacement_list.append(tst_response)
            self.pum_drivealign_to_displacement_list.append(pum_response)
            self.uim_drivealign_to_displacement_list.append(uim_response)

        return uim_response, pum_response, tst_response

    def drivealign_to_longitudinal_displacement(self, frequencies):
        """
        This computes the transfer function from the input of the DRIVEALIGN
        filter bank of each stage to displacement of the test mass
        where "longitudinal" is defined as in the traditional SUS
        Euler Basis: positive longitudinal displacement is along a
        vector perpendicular to the plane of the HR surface
        (positive ETMX displacement is in the -X global IFO direction,
        positive ITMY displacement is in the +Y global IFO direction).

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage
        tst_response : `complex128`, array-like
            transfer function response of the TST stage

        """

        # Digital out to displacement of the TST stage by each of the
        # SUS stages
        [uim_response,
         pum_response,
         tst_response] = self.digital_out_to_displacement(frequencies)

        # Need to add in the DRIVEALIGN bank for each stage
        # Like before, we can reuse the pfilt variable if the preceeding
        # stage feedback goes to the same SUS
        tst_drive_align_filter_response, pfilt = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_drive_align_bank, self.tst_drive_align_modules[0],
                self.tst_drive_align_gain, frequencies)
        pum_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_drive_align_bank, self.pum_drive_align_modules[0],
                self.pum_drive_align_gain, frequencies, pfilt)[0]
        uim_drive_align_filter_response = \
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_drive_align_bank, self.uim_drive_align_modules[0],
                self.uim_drive_align_gain, frequencies)[0]

        uim_response *= uim_drive_align_filter_response
        pum_response *= pum_drive_align_filter_response
        tst_response *= tst_drive_align_filter_response

        return uim_response, pum_response, tst_response

    def drivealign_to_darm_displacement(self, frequencies):
        """
        This computes the transfer function from the input of the DRIVEALIGN
        filter bank of each action stage to DARM by accounting for how
        positive longitudinal drive for each actuation stage pushes the given
        test mass to creates DARM.

        DARM displacement is defined by

        .. math ::

            + DARM = + Delta L \\
            = (Delta L_X - Delta L_Y) \\
            = - (Delta L_EX + Delta L_IX) + (Delta L_EY + Delta L_IY)

        This is particularly useful for computing EPICS records

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage
        tst_response : `complex128`, array-like
            transfer function response of the TST stage

        """

        longitudinal_displacement = (
            self.drivealign_to_longitudinal_displacement(frequencies))

        # Multiply each stage by the DARM feedback sign
        for idx, tf in enumerate(longitudinal_displacement):
            tf *= self.darm_feedback_sign
        darm_displacement = longitudinal_displacement  # rename after DARM sign

        # Return the DARM displacement tuple
        return darm_displacement

    def known_actuation_terms_for_measurement(self, frequencies):
        """
        This method computes all known terms which are divided out of the
        DARM_ERR / SUS_EXC full IFO actuation measurement for each stage
        such that the remaining dimensional actuation strength, H_Ai, can
        be fit by MCMC.

        This computes the transfer function from the input of the DRIVEALIGN
        filter bank (same as the SUS_EXC point) of each stage to DARM
        displacement from any test mass, including everything except the
        N/(drive unit); either amps or volts**2, for which the MCMC will fit.
        The DARM feedback sign of the arm the measurement is taken on since
        we read out the measurement with DARM_ERR.

        This method is essentially computing
        drivealign_to_darm_displacement / dc_gain_Npct * dc_gain_?pct
        where ? is A or V2, but we write all of this out explicitly because
        we want to be able to compute the transfer function without knowing in
        advance anything about NpA or NpV2

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        uim_response : `complex128`, array-like
            transfer function response of the UIM stage, everything but N/ct
        pum_response : `complex128`, array-like
            transfer function response of the PUM stage, everything but N/ct
        tst_response : `complex128`, array-like
            transfer function response of the TST stage, everything but N/ct

        """

        # DRIVEALIGN bank for each stage
        # Like before, we can reuse the pfilt variable if the preceeding
        # stage feedback goes to the same SUS
        tst_drive_align_filter_response, pfilt = (
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.tst_drive_align_bank, self.tst_drive_align_modules[0],
                self.tst_drive_align_gain, frequencies))
        pum_drive_align_filter_response = (
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.pum_drive_align_bank, self.pum_drive_align_modules[0],
                self.pum_drive_align_gain, frequencies, pfilt)[0])
        uim_drive_align_filter_response = (
            compute_digital_filter_response(
                self.dpath(self.sus_filter_file),
                self.uim_drive_align_bank, self.uim_drive_align_modules[0],
                self.uim_drive_align_gain, frequencies)[0])

        # Analog force to length response for each stage from Matlab
        sus_file = self.dpath(self.suspension_file)
        [uim_f2l_response,
         pum_f2l_response,
         tst_f2l_response] = self.matlab_force2length_response(
            sus_file, frequencies)

        # Actuation stage residuals
        A_u_res = self.actuation_stage_residual(frequencies, stage='UIM')
        A_p_res = self.actuation_stage_residual(frequencies, stage='PUM')
        A_t_res = self.actuation_stage_residual(frequencies, stage='TST')

        # All together this will be:
        # DARM feedback sign
        # DRIVEALIGN transfer function
        # SUS actuator gain in units of A/ct or V**2/ct
        # Force-to-length response
        # SUS stage residuals
        uim_response = (self.darm_feedback_sign *
                        uim_drive_align_filter_response *
                        self.uim_dc_gain_Apct() *
                        uim_f2l_response *
                        A_u_res)
        pum_response = (self.darm_feedback_sign *
                        pum_drive_align_filter_response *
                        self.pum_dc_gain_Apct() *
                        pum_f2l_response *
                        A_p_res)
        tst_response = (self.darm_feedback_sign *
                        tst_drive_align_filter_response *
                        self.tst_dc_gain_V2pct() *
                        tst_f2l_response *
                        A_t_res)

        return uim_response, pum_response, tst_response

    def compute_actuation_single_stage(self, frequencies, stage='TST'):
        """
        Compute the actuation function transfer function for a single stage
        (see G1501518). This transfer function is from the DARM control
        input at the SUS user model, or the input to the ISCINF bank, to
        DARM displacement.

        This does not include the OMC to SUS model jump delay

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        stage : `str`, optional
            UIM, PUM or TST (default = 'TST')

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the actuation function

        """

        # Digital output to TST displacement
        # Note that no feedback or output matrix values are applied here
        # Note also that digital_out_to_displacement does not have the
        # OMC to SUS delay
        [uim_response,
         pum_response,
         tst_response] = self.digital_out_to_displacement(frequencies)

        # All SUS digital filters
        [uim_digital_filter_response,
         pum_digital_filter_response,
         tst_digital_filter_response] = self.sus_digital_filters_response(
            frequencies)

        # Choose the right stage
        if stage in ['UIM', 'L1']:
            sus_response = uim_response * uim_digital_filter_response
        elif stage in ['PUM', 'L2']:
            sus_response = pum_response * pum_digital_filter_response
        elif stage in ['TST', 'L3']:
            sus_response = tst_response * tst_digital_filter_response
        else:
            raise ValueError('stage must be UIM, PUM, TST, L1, L2, or L3')

        sus_response *= self.darm_feedback_sign

        # Everything *above* here is modelling the physical actuator that we
        # have. However, the calibration group's convention is that A in their
        # loop drawings is minus the physical actuator (which allows the
        # explicit writing of the minus sign in the loop drawing to indicate
        # negative feedback). Ideally we'd just put
        # A = -1 * (TOP + UIM + PUM + TST),
        # but the actuation products below (which are used for other things
        # downstream) are expecting to receive minus of each stage of the
        # physical actuator. So, we multiply every stage by -1, and then sum
        # them up, and the result will be that A is negative of the physical
        # actuator. JCD_26Mar2019
        # See more details in T1800456.
        sus_response *= -1

        return sus_response


class DARMActuationModel(Model):
    """
    An DARM actuation model object

    This is a class to set up the model for the DARM loop from a
    configuration file with all the information about where the data is stored

    """

    def __init__(self, config):
        super().__init__(config, measurement='actuation')
        self.xarm = self.yarm = None
        if 'actuation_x_arm' in self._config:
            self.xarm = ActuationModel(config, measurement='actuation_x_arm')
        if 'actuation_y_arm' in self._config:
            self.yarm = ActuationModel(config, measurement='actuation_y_arm')

    def darm_output_matrix_values(self):
        """Turns the output matrix values into an array for the QUAD SUS

        """

        output_matrix = np.zeros((2, 4))
        for m in range(len(output_matrix[:, 0])):
            for n in range(len(output_matrix[0, :])):
                if m == 0 and self.darm_feedback_x[n] == 'ON':
                    output_matrix[m, n] = self.darm_output_matrix[0]
                elif m == 1 and self.darm_feedback_y[n] == 'ON':
                    output_matrix[m, n] = self.darm_output_matrix[1]

        return output_matrix

    def stage_super_actuator(self, frequencies, stage='TST', syserr_dict=None):
        """
        Compute the super actuator transfer function for a specific stage.
        In this case, the "stage super actuator" is created by choosing a
        specific stage and then for each QUAD, the stage transfer function to
        DARM is summed together.

        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        The OMC to SUS delay is included in this transfer function.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        stage : `str`, optional
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'
        syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        super_actuation : `complex128`, array-like
            transfer function response of the actuation function

        """

        output_matrix = self.darm_output_matrix_values()

        super_actuation = np.zeros(len(frequencies), dtype='complex128')

        stage_idx = ['top', 'uim', 'pum', 'tst'].index(stage.lower())
        for arm_idx, arm in enumerate(['x', 'y']):
            if output_matrix[arm_idx, stage_idx] != 0.0:
                assert stage_idx > 0, 'top has not been implemented'

                if hasattr(self, f'{arm}arm') is False:
                    raise ValueError(
                        'Must provide an ActuationModel object')
                else:
                    this_arm = getattr(self, f'{arm}arm')

                single_stage = this_arm.compute_actuation_single_stage(
                        frequencies, stage=stage.upper())

                if (syserr_dict is not None and
                        ['xarm', 'yarm'][arm_idx] in syserr_dict and
                        stage.upper() in syserr_dict[['xarm', 'yarm'][arm_idx]]):
                    single_stage *= (
                        syserr_dict[['xarm', 'yarm'][arm_idx]][stage.upper()])

                super_actuation += (
                    output_matrix[arm_idx, stage_idx] * single_stage)

        # OMC to SUS model jump delay, sending DARM_CTRL from the omc
        # front-end model via IPC to any QUAD SUS model, identical for any
        # QUAD, either at the corner or end.
        # Note that SUS to IOP, IOP to analog, and unknown delays have already
        # been applied in compute_actuation_single_stage.
        # For measurement confirmation of computational time delays see
        # G1601472.
        omc_to_sus_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        super_actuation *= omc_to_sus_delay_response

        return super_actuation

    def stage_super_actuator_drivealign(self, frequencies, stage='TST',
                                        syserr_dict=None):
        """
        Compute the super actuator transfer function for a specific stage.
        In this case, the "stage super actuator" is created by choosing a
        specific stage and then for each QUAD, the stage transfer function to
        DARM is summed together.

        This transfer function is from the input of the DRIVEALIGN filter bank
        to meters sensed by the IFO. This method assumes that the signal
        feedback to a single stage would be positive, but if the signal is sent
        to both arms (like a DARM signal) then X and Y are 180 degrees out of
        phase.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        stage : `str`
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'
        syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        super_actuation : `complex128`, array-like
            transfer function response of the actuation function
        """

        assert stage.lower() != 'top', 'top has not been implemented'

        # Get the output matrix values
        output_matrix = self.darm_output_matrix_values()

        # Get the stage index
        stage_idx = ['top', 'uim', 'pum', 'tst'].index(stage.lower())

        # We have two scenarios:
        # 1) Both arms are used for servo control. X and Y arms receive the
        # same signal but 180 degrees out of phase, so here we end up
        # SUBTRACTING the Y arm from X arm due to this 180 degrees difference
        # 2) Only one arm uses feedback control. We want to maintain the
        # historical infrastructure for single-arm feedback, so we don't
        # need to account for any signs when combining arm contributions.
        # There may be a cleaner way to code this...
        if output_matrix[0, stage_idx] != 0 and output_matrix[1, stage_idx] != 0:
            # Check that we have attributes for both arms
            if hasattr(self, 'xarm') is False or hasattr(self, 'yarm') is False:
                raise ValueError('Must provide an ActuationModel object for both arms')

            xarm_contrib = (
                self.xarm.drivealign_to_darm_displacement(frequencies)[stage_idx-1])
            yarm_contrib = (
                self.yarm.drivealign_to_darm_displacement(frequencies)[stage_idx-1])

            if syserr_dict is not None:
                if 'xarm' in syserr_dict and stage.upper() in syserr_dict['xarm']:
                    xarm_contrib *= syserr_dict['xarm'][stage.upper()]
                if 'yarm' in syserr_dict and stage.upper() in syserr_dict['yarm']:
                    yarm_contrib *= syserr_dict['yarm'][stage.upper()]

            super_actuation = xarm_contrib - yarm_contrib
        else:
            for arm_idx, arm in enumerate(['x', 'y']):
                if output_matrix[arm_idx, stage_idx] != 0.0:
                    if hasattr(self, f'{arm}arm') is False:
                        raise ValueError('Must provide an ActuationModel object')
                    this_arm = getattr(self, f'{arm}arm')

                    super_actuation = this_arm.drivealign_to_darm_displacement(
                        frequencies)[stage_idx-1]

                    if (syserr_dict is not None and
                            f'{arm}arm' in syserr_dict and
                            stage.upper() in syserr_dict[f'{arm}arm']):
                        super_actuation *= syserr_dict[f'{arm}arm'][stage.upper()]

        return super_actuation

    def arm_super_actuator(self, frequencies, arm='x', syserr_dict=None):
        """
        Compute the super actuator transfer function for a specific arm.
        In this case, the "arm super actuator" is created by choosing a
        specific arm and then for each QUAD, the arm transfer function to
        DARM is summed together.

        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        The OMC to SUS delay is included in this transfer function.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        arm : `str`
            arm for the calculation, 'x' or 'y'
        syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        super_actuation : `complex128`, array-like
            transfer function response of the actuation function

        """

        output_matrix = self.darm_output_matrix_values()

        super_actuation = np.zeros(len(frequencies), dtype='complex128')

        arm_idx = ['x', 'y'].index(arm.lower())
        for stage_idx, stage in enumerate(['top', 'uim', 'pum', 'tst']):
            if output_matrix[arm_idx, stage_idx] != 0.0:
                assert stage_idx > 0, 'top has not been implemented'

                if hasattr(self, f'{arm}arm') is False:
                    raise ValueError(
                        'Must provide an ActuationModel object')
                this_arm = getattr(self, f'{arm}arm')

                single_stage = this_arm.compute_actuation_single_stage(
                        frequencies, stage=stage.upper())

                if (syserr_dict is not None and
                        ['xarm', 'yarm'][arm_idx] in syserr_dict and
                        stage.label() in syserr_dict[['xarm',
                                                      'yarm'][arm_idx]]):
                    single_stage *= (
                        syserr_dict[['xarm', 'yarm'][arm_idx]][stage.upper()])

                super_actuation += (
                    output_matrix[arm_idx, stage_idx] * single_stage)

        # OMC to SUS model jump delay, sending DARM_CTRL from the omc
        # front-end model via IPC to any QUAD SUS model, identical for any
        # QUAD, either at the corner or end.
        # Note that SUS to IOP, IOP to analog, and unknown delays have already
        # been applied in compute_actuation_single_stage.
        # For measurement confirmation of computational time delays see
        # G1601472.
        omc_to_sus_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        super_actuation *= omc_to_sus_delay_response

        return super_actuation

    def compute_actuation(self, frequencies, syserr_dict=None):
        """
        Compute the entire actuation function transfer function (see G1501518).
        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        syserr_dict : `dict`, optional
            dict of multiplicative values, ex.:
            {'xarm': {'UIM': `complex`, array-like}}

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the actuation function

        """

        darm_actuation = np.zeros(len(frequencies), dtype='complex128')

        # This has the OMC to SUS time delay
        for stage_idx, stage in enumerate(['top', 'uim', 'pum', 'tst']):
            darm_actuation += self.stage_super_actuator(
                frequencies, stage=stage.upper(), syserr_dict=syserr_dict)

        return darm_actuation
