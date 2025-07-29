# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2022)
#
# This file is part of pyDARM.

import numpy as np
from scipy import signal

from .utils import load_foton_export_tf, digital_delay_filter
from .digital import daqdownsamplingfilters
from .model import Model
from .darm import DARMModel


class CALCSModel(DARMModel):

    def __init__(self, config, calcs=None):
        """
        Initialize a CALCSModel object

        Note that any string or path to file string in `calcs` will
        overwrite anything in the `config` parameter string or path to file
        """
        super().__init__(config)
        if 'calcs' in self._config:
            self.calcs = Model(config, measurement='calcs')
        if calcs is not None:
            self.calcs = Model(calcs, measurement='calcs')
        if not hasattr(self, 'calcs'):
            raise ValueError('No CALCS parameters have been defined')

    def optical_response_ratio(self, frequencies):
        """
        This computes (opt resp) / (opt resp)_foton

        It is a bit confusing because the FOTON filter is the inverse
        sensing function, so we'll be multiplying the true optical
        response from the model by the FOTON transfer function.

        In T1900169, in the definition of C/C_CALCS, the last three
        terms are
        .. math :: (opt resp)/(opt resp)_foton * (LP_foton/LP) * LP
        and this method returns this combination since the export from
        FOTON gives the full combination of
        .. math :: LP_foton / (opt resp)_foton

        Note that (LP_foton/LP) is the "IIR warping"

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the optical response ratio

        Returns
        -------
        foton_inv_sensing_interp : `complex128`, array-like
            ratio of interpolated values
        """

        # We need the coupled cavity LTI object
        coupled_cavity = self.sensing.optical_response(
            self.sensing.coupled_cavity_pole_frequency,
            self.sensing.detuned_spring_frequency,
            self.sensing.detuned_spring_q,
            pro_spring=self.sensing.is_pro_spring)

        # load inverse sensing data from foton file export (1/SRC_D2N)
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(self.calcs.foton_invsensing_tf))

        # apply gain, default is 1.0
        invsensing_gain = getattr(self, 'invsensing_gain', 1.0)
        foton_tf *= invsensing_gain

        # Take ratio of true optical response / foton response where
        # "foton response" is already the approximated
        # LP_foton / (opt resp)_foton, so we just need to multiply the two
        # terms
        opt_response_ratio = (
            signal.freqresp(coupled_cavity, 2.0*np.pi*foton_freq)[1] *
            foton_tf)

        # interpolate to the requested frequencies
        opt_response_ratio_interp = np.interp(frequencies,
                                              foton_freq,
                                              opt_response_ratio)

        return opt_response_ratio_interp

    def sus_response_ratio(self, frequencies, arm, stage):
        """
        This computes (sus resp) / (sus resp)_foton

        See T1900169 definition of delta A_mn

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the optical response ratio
        arm : str, `x` or `y`
        stage : str `UIM`, `PUM`, or `TST`

        Returns
        -------
        response_ratio : `complex128`, array-like
            ratio of interpolated values
        """

        # load FOTON suspension dynamics filter
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(getattr(self.calcs,
                               f'{arm.lower()}arm_{stage.lower()}_analog')))

        if arm.lower() == 'x':
            arm_act = self.actuation.xarm
        elif arm.lower() == 'y':
            arm_act = self.actuation.yarm
        else:
            raise ValueError('The accepted values for arm is x or y')

        # get true suspension dynamics
        [uim, pum, tst] = arm_act.matlab_force2length_response(
            arm_act.suspension_file, foton_freq)

        if stage.lower() == 'uim':
            ratio = uim / foton_tf
        elif stage.lower() == 'pum':
            ratio = pum / foton_tf
        elif stage.lower() == 'tst':
            ratio = tst / foton_tf
        else:
            raise ValueError('stage must be uim, pum or tst')

        # interpolate to the requested frequencies
        response_ratio = np.interp(frequencies, foton_freq, ratio)

        return response_ratio

    def C_corr(self, frequencies):
        """
        Compute delta C = delay*(opt resp)/(opt resp)_foton*C_r

        The inverse of this transfer function is multiplied by
        DELTAL_RESIDUAL as the GDS correction.

        We need to divide out the normalized optical response FOTON filter
        only and be sure to include 1 16k clock cycle delay from the model
        jump OMC to CAL-CS. There is an optical
        gain factor in the front end model, but it is fine to leave this in
        place. The output is basically C_pydarm / C_foton, and GDS will need to
        either divide the DELTAL_RESIDUAL data by this function or invert the output
        of this function and multiply by the DELTAL_RESIDUAL data.

        This is delay*(opt resp)/(opt resp)_foton*C_r (see T1900169-v5 eq 33)

        This is also known as C_corr or delta C in T1900169

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction
        """

        # Residual sensing function transfer function
        # This is everything in sensing except the optical gain and response
        C_res = self.sensing.sensing_residual(frequencies)

        # we will need to apply a delay because when it is inverted in GDS
        # this will become an advance (the correct thing to do)
        omc_to_calcs_response = (
            signal.dfreqresp(digital_delay_filter(1, 2**14),
                             2.0*np.pi*frequencies/2**14)[1])

        # get the optical response ratio between FOTON and pyDARM
        opt_response_ratio = self.optical_response_ratio(frequencies)

        # the final correction is the sensing model divided by the interpolated
        # foton filter
        correction = (omc_to_calcs_response *
                      opt_response_ratio *
                      C_res)

        return correction

    def drivealign_out_to_longitudinal_displacement(
            self, frequencies, arm, stage):
        """
        CALCS representation of the transfer function from the
        DRIVEALIGN bank to longitudinal displacement of the test
        mass.
        Units are m/ct = (N/ct) * (m/N)


        The gain (N/ct) of the CALCS model is assumed to be exactly the same
        as what is in the reference model, so that is used. If any digital
        gain is present as <arm>_<stage>_analog_gain, then it will be
        applied here.

        If there is anything in the "coiloutf" key-value pair, then this
        transfer function is also used, but this would be used only in
        special circumstances.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the CALCS approximated longitudinal
            actuation of the test mass from the given stage
        arm : `str`
            arm for the calculation, 'x' or 'y'
        stage : `str`
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'

        Returns
        -------
        out_tf : `complex128`, array-like
            CALCS approximation of the DRIVEALIGN output to displacement
        """

        # The pieces of the actuator are multiplicative to obtain the final
        # result so we need to start with unity transfer functions and
        # change them only if a user has supplied a FOTON transfer
        # function export. The tf_ana_interp will be filled in by the FOTON
        # export of the SUS response. The tf_dig_interp will only be used if
        # there is CALCS COILOUTF content.
        tf_dig_interp = np.ones(len(frequencies), dtype='complex128')
        tf_ana_interp = np.ones(len(frequencies), dtype='complex128')

        # Get the coiloutf and analog exports if they exist
        if hasattr(self.calcs, f'{arm.lower()}arm_{stage.lower()}_coiloutf'):
            val = getattr(
                self.calcs, f'{arm.lower()}arm_{stage.lower()}_coiloutf')
            if val != '':
                [f, tf_dig] = load_foton_export_tf(self.dpath(val))
                tf_dig_interp = np.interp(frequencies, f, tf_dig)
        if hasattr(self.calcs, f'{arm.lower()}arm_{stage.lower()}_analog'):
            val = getattr(
                self.calcs, f'{arm.lower()}arm_{stage.lower()}_analog')
            if val != '':
                [f, tf_ana] = load_foton_export_tf(self.dpath(val))
                tf_ana_interp = np.interp(frequencies, f, tf_ana)

        # Get the CALCS actuation output matrix (different then the DARM output
        # matrix)
        # TODO: this is -1 for X and I think +1 for Y; why is this?
        if hasattr(self.calcs, f'{arm.lower()}arm_output_matrix'):
            idx = ['top', 'uim', 'pum', 'tst'].index(stage.lower())
            out_mtrx = getattr(self.calcs,
                               f'{arm.lower()}arm_output_matrix')[idx]
        else:
            out_mtrx = 0

        # put in the gain and the DARM feedback sign
        # FOTON export is in m/N, here we apply the N/ct from the model
        # assuming that this has been replicated perfectly in CALCS.
        if (getattr(self.actuation, f'{arm.lower()}arm') is not None and
                stage.lower() in ['uim', 'pum', 'tst']):
            if ((stage.lower() in ['uim', 'pum'] and
                    hasattr(getattr(self.actuation, f'{arm.lower()}arm'),
                            f'{stage.lower()}_npa') and
                    getattr(getattr(self.actuation, f'{arm.lower()}arm'),
                            f'{stage.lower()}_npa') != '') or
                    (stage.lower() == 'tst' and
                        hasattr(getattr(self.actuation, f'{arm.lower()}arm'),
                                f'{stage.lower()}_npv2') and
                        getattr(getattr(self.actuation, f'{arm.lower()}arm'),
                                f'{stage.lower()}_npv2') != '')):
                act_arm_model = getattr(self.actuation, f'{arm.lower()}arm')
                if stage.lower() == 'uim':
                    tf_ana_interp *= act_arm_model.uim_dc_gain_Npct()
                elif stage.lower() == 'pum':
                    tf_ana_interp *= act_arm_model.pum_dc_gain_Npct()
                else:
                    tf_ana_interp *= act_arm_model.tst_dc_gain_Npct()

        # apply CALCS digital gain, default is 1
        act_gain = getattr(self, f'{arm}arm_{stage.lower()}_analog_gain', 1.0)
        tf_ana_interp *= act_gain

        out_tf = (out_mtrx *
                  tf_dig_interp *
                  tf_ana_interp)

        return out_tf

    def drivealign_out_to_darm_displacement(self, frequencies, arm, stage):
        """
        CALCS representation of the SUS_EXC DRIVEALIGN point to DARM
        displacement transfer function.

        Units are m/ct = (N/ct) * (m/N)


        The gain (N/ct) of the CALCS model is assumed to be exactly the same
        as what is in the reference model, so that is used.

        If there is anything in the "coiloutf" key-value pair, then this
        transfer function is also used, but this would be used only in
        special circumstances.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies
        arm : `str`
            arm for the calculation, 'x' or 'y'
        stage : `str`
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'

        Returns
        -------
        tf : `complex128`, array-like
            CALCS approximation of the DRIVEALIGN output to DARM displacement
        """

        if (getattr(self.actuation, f'{arm.lower()}arm') is None):
            raise ValueError('Must provide a valide arm object')

        act_arm_model = getattr(self.actuation, f'{arm.lower()}arm')

        tf = (act_arm_model.darm_feedback_sign *
              self.drivealign_out_to_longitudinal_displacement(
                  frequencies, arm, stage))

        return tf

    def compute_actuation_single_stage(self, frequencies, arm, stage):
        """
        A_n,calcs

        CALCS approximation of a specific arm, stage from input to SUS ISCINF
        to DARM (and therefore does not include the OMC to CALCS delay)
        displacement. See T1900169


        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the CALCS approximated DARM actuation
        arm : `str`
            arm for the calculation, 'x' or 'y'
        stage : `str`
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'

        Returns
        -------
        calcs_stage_actuation : `complex128`, array-like
            CALCS approximation of SUS model ISCINF input to DARM displacement
            transfer function
        """

        # Assume the same as in-loop DARM output matrix
        # only used as determining if this is non-zero
        output_matrix = self.actuation.darm_output_matrix_values()

        # initialize zeros for the output
        calcs_stage_actuation = np.zeros(len(frequencies), dtype='complex128')

        arm_idx = ['x', 'y'].index(arm.lower())
        stage_idx = ['top', 'uim', 'pum', 'tst'].index(stage.lower())
        if (output_matrix[arm_idx, stage_idx] != 0.0):
            assert stage_idx > 0, 'top has not been implemented'

            # Model SUS filters
            arm_obj = getattr(self.actuation, f'{arm}arm')
            dig_filt = arm_obj.sus_digital_filters_response(frequencies)

            # This is the CALCS DARM displacement for this arm and stage
            drivealign_out_to_disp = self.drivealign_out_to_darm_displacement(
                frequencies, arm=arm, stage=stage)

            calcs_stage_actuation = (dig_filt[stage_idx - 1] *
                                     drivealign_out_to_disp)

        return calcs_stage_actuation

    def stage_super_actuator(self, frequencies, stage='TST'):
        """
        Compute the super actuator transfer function for a specific stage as
        estimated by the CALCS model.
        In this case, the "stage super actuator" is created by choosing a
        specific stage and then for each QUAD, the stage transfer function to
        DARM is summed together.

        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        stage : `str`, optional
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the actuation function
        """

        # Assume the same as in-loop DARM output matrix
        output_matrix = self.actuation.darm_output_matrix_values()

        super_actuation = np.zeros(len(frequencies), dtype='complex128')

        stage_idx = ['top', 'uim', 'pum', 'tst'].index(stage.lower())
        for arm_idx, arm in enumerate(['x', 'y']):
            if output_matrix[arm_idx, stage_idx] != 0.0:
                assert stage_idx > 0, 'top has not been implemented'

                single_stage = self.compute_actuation_single_stage(
                        frequencies, arm=arm, stage=stage.upper())

                super_actuation += (
                    output_matrix[arm_idx, stage_idx] * single_stage)

        return super_actuation

    def arm_super_actuator(self, frequencies, arm='x'):
        """
        Compute the super actuator transfer function for a specific arm.
        In this case, the "arm super actuator" is created by choosing a
        specific arm and then for each QUAD, the arm transfer function to
        DARM is summed together.

        This transfer function is from DARM_CTRL to meters sensed by the IFO.
        Note that the sign of the DARM_ERR signal is dependent upon which arm
        is under control.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        arm : `str`, optional
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'

        Returns
        -------
        super_actuation : `complex128`, array-like
            transfer function response of the actuation function
        """

        # Assume the same as in-loop DARM output matrix
        output_matrix = self.actuation.darm_output_matrix_values()

        super_actuation = np.zeros(len(frequencies), dtype='complex128')

        arm_idx = ['x', 'y'].index(arm.lower())
        for stage_idx, stage in enumerate(['top', 'uim', 'pum', 'tst']):
            if output_matrix[arm_idx, stage_idx] != 0.0:
                assert stage_idx > 0, 'top has not been implemented'

                single_stage = self.compute_actuation_single_stage(
                        frequencies, arm=arm, stage=stage.upper())

                super_actuation += (
                    output_matrix[arm_idx, stage_idx] * single_stage)

        return super_actuation

    def gds_actuation_correction(self, frequencies, stage, daqdownsample=True):
        """
        Compute the correction to the CAL-CS output for GDS. Note that this
        implicitly assumes that the front end digital filters in CALCS is the
        same as that in the SUS path!

        This is also more complicated than sensing because there is a single
        channel for a given stage that accounts for BOTH arms; e.g.,
        ${IFO}:CAL-DELTAL_CTRL_${STAGE}_DBL_DQ takes input from both x and y
        arms using an output matrix.

        This is (A_{xn}+A_{yn})/(A_{xn,calcs}+A_{yn,calcs})/(F*delay)
        where n is the stage, calcs denotes FOTON implementation of an actuator
        F is the DAQ downsampling filter (on by default), and delay of the 1
        16384 clock cycle delay going from OMC to CALCS

        See T1900169, definition of delta A_n

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction
        stage : `str`
            SUS stage for the calculation, 'UIM', 'PUM', or 'TST'
        daqdownsample : `bool`, optional
            When True (default), the 16k-4k daqdownsample is applied in
            GDS actuation correction

        Returns
        -------
        correction : `complex128`, array-like
            transfer function response of the correction
        """

        # ideal model sum of actuators for A_{xn} and A_{yn}
        # this DOES NOT include the OMC to SUS delay
        A_n = self.actuation.stage_super_actuator(frequencies,
                                                  stage=stage.upper())

        # CALCS approximate for A_{xn,calcs} and A_{yn,calcs}
        # this DOES include the OMC to CALCS delay
        A_n_calcs = self.stage_super_actuator(frequencies,
                                              stage=stage.upper())

        # 1 clock cycle delay transfer function for OMC to CALCS
        omc_to_calcs_response = (
            signal.dfreqresp(digital_delay_filter(1, 16384),
                             2.0*np.pi*frequencies/16384)[1])

        if daqdownsample:
            # DAQ downsampling filters are applied so we need to account
            # for this
            daqdownsampling = signal.dfreqresp(
                daqdownsamplingfilters(16384, 4096, 'biquad', 'v3'),
                2.0*np.pi*frequencies/16384)[1]
        else:
            daqdownsampling = 1

        # This is \delta A_n
        # note that A_n already includes the OMC to SUS response
        correction = ((A_n / A_n_calcs) *
                      (1 / (daqdownsampling * omc_to_calcs_response)))

        return correction

    def calcs_darm_actuation(self, frequencies):
        """
        Compute the CALCS approximated DARM actuation. This method implicitly
        assumes that the CALCS DARM output matrix and actuation digital
        filtering matches the installed in-loop DARM ouput matrix and actuation
        digital filtering.

        See T1900169, definition of A_CALCS

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the CALCS approximated DARM actuation

        Returns
        -------
        calcs_actuation : `complex128`, array-like
            Residual phase after removing the simulated delay
        """

        # Start with zeros
        calcs_actuation = np.zeros(len(frequencies), dtype='complex128')

        # This has the OMC to CALCS time delay
        for stage_idx, stage in enumerate(['top', 'uim', 'pum', 'tst']):
            calcs_actuation += self.stage_super_actuator(
                frequencies, stage=stage.upper())

        return calcs_actuation

    def gds_sensing_correction(self, frequencies):
        """
        Compute 1 / C_corr = C_foton / C see T1900169.

        For the sensing path, GDS sensing correction = 1 / C_corr. This is
        to be multiplied into DELTAL_RESIDUAL

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction
        """

        return 1 / self.C_corr(frequencies)

    def A_corr(self, frequencies, daqdownsample=True):
        """
        Compute total DARM actuator A_corr = A / A_foton (aka delta A),
        see T1900169.

        This is more complicated than computing C_corr, since the GDS actuation
        correction is applied to each stage separately, so we cannot just sum
        the corrections and multiply by a common factor. Instead, we compute
        the modeled (true) DARM actuation, and divide by the CALCS
        (approximate) DARM actuation. We also account for the OMC to CALCS
        delay and the possibility for DAQ downsampling.

        DAQ downsample is an option here because if you want to create
        delta L_ctrl from ${IFO}:CAL-DELTAL_CTRL_DBL_DQ, then we need to
        use daqdownsampling = True because the channel that is read has
        been downsampled. When computing the delay between CAL-DELTAL_CTRL
        and CAL-DELTAL_RESIDUAL to improve CAL-DELTAL_EXTERNAL, however, one
        does not need daqdownsampling (see discussion in sec III of
        T1900169).

        Both products are using the CALCS copy of DARM_CTRL and therefore need
        the delay (OMC to CALCS)

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the GDS sensing correction
        daqdownsample : `bool`, optional
            When True (default), the 16k-4k daqdownsample is applied in A_corr

        Returns
        -------
        A_corr : `complex128`, array-like
            transfer function response of the correction
        """

        if daqdownsample:
            # DAQ downsampling filters are applied so we need to account
            # for this
            daqdownsampling = signal.dfreqresp(
                daqdownsamplingfilters(16384, 4096, 'biquad', 'v3'),
                2.0*np.pi*frequencies/16384)[1]
        else:
            daqdownsampling = 1

        # we will need to apply a delay because when it is inverted in GDS
        # this will become an advance (the correct thing to do)
        omc_to_calcs_response = (
            signal.dfreqresp(digital_delay_filter(1, 16384),
                             2.0*np.pi*frequencies/16384)[1])

        A = self.actuation.compute_actuation(frequencies)
        A_calcs = self.calcs_darm_actuation(frequencies)

        A_corr = ((A / A_calcs) *
                  (1 / (daqdownsampling * omc_to_calcs_response)))

        return A_corr

    def sensing_actuation_delay(self, frequencies, clock=False):
        """
        Compute the delay based on the GDS sensing and actuation correction in
        units of seconds delay or (if clock=True) in units of 16384
        samples/sec, i.e., 1 16384 Hz clock delay = 6.1035e-5 s. Positive
        indicates a delay, negative indicates an advance

        See T1900169, sec III "method 1"

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to model the phase delay
        clock : `boolean`, optional
            if clock is True, then the output delay_fit and residual will
            be computed and rounded to the nearest number of integer clock
            cycles (16384)

        Returns
        -------
        delay : float
            Units of seconds or 16384 Hz clock cycles (if clock=True)
        """

        # We use the C_corr = \delta C and A_corr = \delta A values from
        # T1900169, but note that we TURN OFF the DAQ downsample here
        # because the path that is summed in CALCS does not have the DAQ
        # downsampling
        C_corr = self.C_corr(frequencies)
        A_corr = self.A_corr(frequencies, daqdownsample=False)

        delay = -np.angle(C_corr*A_corr) / (2.0*np.pi*frequencies)

        if clock is True:
            delay = delay * 16384

        return delay

    def deltal_ext_whitening(self, frequencies):
        """
        Compute the interpolated transfer function of the DELTAL_EXTERNAL
        export from FOTON

        If no export file is provided in the configuration, this method
        will return an array of ones

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the interpolation

        Returns
        -------
        whitening_interp : `complex128`, array-like
            transfer function response of the calibration
        """

        if (hasattr(self.calcs, 'foton_deltal_whitening_tf') and
                getattr(self.calcs, 'foton_deltal_whitening_tf') != ''):
            foton_freq, foton_tf = load_foton_export_tf(
                self.dpath(self.calcs.foton_deltal_whitening_tf))
            whitening_interp = np.interp(frequencies,
                                         foton_freq,
                                         foton_tf)
        else:
            whitening_interp = np.ones(len(frequencies), dtype='complex128')

        return whitening_interp

    def calcs_dtt_calibration(self, frequencies, include_whitening=True,
                              strain_calib=False, save_to_file=None, fmt=None):
        """
        Compute the calibration transfer function, dL_pyDARM / dL_CALCS
        for the main control room calibrated sensitivity curve. One can save
        this data to a file with the needed frequency, dB magnitude, and
        degrees phase columns, and apply it to a DTT template.

        See T1900169 section IV

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the CAL_DELTAL_EXTERNAL DTT
            calibration
        include_whitening : `bool`, optional
            if the whitening filter is on (default), then we'd like to remove
            its effect so by default this divides out the whitening filter
        strain_calib : `bool`, optional
            the output defaults to dL_pyDARM/dL_CALCS, so that we can recalibrate
            CAL-DELTAL_EXTERNAL. If this option is True, then the output is
            h_pyDARM/dL_CALCS
        save_to_file : `str`, optional
            Filename (ASCII) to save the data from this result. Note:
            the default file columns are
            <frequency> <magnitude (dB)> <phase (deg)>
        fmt : `str`, optional
            if save_to_file is used, then this is the output format. Options
            are 'dB,deg' (default), 'mag,deg', 'dB,rad', 'mag,rad', or 're,im'.
            If none is given, then the default is used

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the calibration
        """

        # This is C_r*delay*(opt resp)/(opt resp)_foton
        C_corr = self.C_corr(frequencies)

        # Remember that A_corr should not have a DAQ downsample since
        # the path that is summed does not have the DAQ downsample in it
        A_corr = self.A_corr(frequencies, daqdownsample=False)

        # Whitening filter
        whitening_interp = self.deltal_ext_whitening(frequencies)

        if not include_whitening:
            whitening_interp = 1

        # Foton delay filter
        foton_freq, foton_tf = load_foton_export_tf(
            self.dpath(self.calcs.foton_delay_filter_tf))
        delay_interp = np.interp(frequencies, foton_freq, foton_tf)

        # Model loop gain CDA
        G = self.compute_darm_olg(frequencies)

        calib = ((1 / whitening_interp) *
                 (1 / C_corr) *
                 ((1.0 + G) /
                  (1.0 + G*delay_interp/(C_corr*A_corr))))

        if strain_calib:
            calib /= self.sensing.mean_arm_length()

        # Save to file and use the fmt options if given
        # default is to save as dB magnitude and degrees phase
        if save_to_file is not None:
            col1 = frequencies
            col2 = 20.0*np.log10(np.abs(calib))
            col3 = np.angle(calib, deg=True)

            if fmt is not None:
                fmt_opt = fmt.split(',')
                if len(fmt_opt) != 2:
                    raise ValueError('Wrong formatting for fmt')
                if fmt_opt[0] == 'mag':
                    col2 = np.abs(calib)
                elif fmt_opt[0] == 're':
                    col2 = np.real(calib)
                if fmt_opt[1] == 'rad':
                    col3 = np.angle(calib, deg=False)
                elif fmt_opt[1] == 'im':
                    col3 = np.imag(calib)

            np.savetxt(save_to_file,
                       np.array([col1,
                                 col2,
                                 col3]).T,
                       fmt='%.7g')

        return calib

    def deltal_ext_pcal_correction(self, frequencies, **kwargs):
        """
        Compute the calibration transfer function, dL_pyDARM / dL_Pcal
        for determining the response function systematic error

        See T1900169 section V

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the CAL_DELTAL_EXTERNAL DTT
            calibration
        kwargs : optional
            values are passed to `calcs.calcs_dtt_calibration()` and
            `pcal.compute_pcal_correction()`

        Returns
        -------
        tf : `complex128`, array-like
            transfer function resposne of the correction factor
        """

        endstation = kwargs.pop('endstation', False)
        include_dewhitening = kwargs.pop('include_dewhitening', True)
        arm = kwargs.pop('arm', 'REF')

        deltal_ext = self.calcs_dtt_calibration(frequencies, **kwargs)
        pcal_corr = self.pcal.compute_pcal_correction(
            frequencies,
            endstation=endstation,
            include_dewhitening=include_dewhitening,
            arm=arm)

        tf = deltal_ext / pcal_corr

        return tf

    def compute_epics_records(self, gds_pcal_endstation=False,
                              gds_sus_endstation=False, gds_darm_omc=False,
                              exact=False):
        """Generate EPICS values for CALCS front-end model time dependent
        correction factors

        This is a LIGO specific function for generating front end
        calibration EPICS records. The GDS pipeline reads these EPICS records
        and together with channels read from frames computes TDCFs. If
        GDS reads channels from the end station or OMC models rather than
        CALCS, then the CALCS model will need to get phase values assigned to
        DEMODs in order to have the proper synchronization. The default
        assumes that GDS reads all channels from CALCS

        See T1700106-v10 and G1601472 for additional details

        Parameters
        ----------
        gds_pcal_endstation : `bool`, optional
            When false (default), the correction is computed for CAL-CS PCAL
            channel, which includes 1 16k clock cycle delay that we must
            compensate (undo). Otherwise, when true, the correction is computed
            at the end station, which does not include 1 16k clock cycle delay
        gds_sus_endstation : `bool`, optional
            When false (default), the correction is computed for CAL-CS SUS
            channel, which includes 1 16k clock cycle delay that we must
            compensate (undo). Otherwise, when true, the correction is computed
            at the end station, which does not include 1 16k clock cycle delay
        gds_darm_omc : `bool`, optional
            When false (default), the correction is computed for CAL-CS DARM ERR
            channel, which includes 1 16k clock cycle delay that we must
            compensate (undo). Otherwise, when true, the correction is computed
            at the OMC, which does not include 1 16k clock cycle delay
        exact : `bool`, optional
            When True, the exact TDCF transfer function calculations
            are updated in the output dictionary. This will append new
            values to the output dictionary

        Returns
        -------
        out : dict
            Dictionary of EPICS records

        """
        freq_indicies = {
            'f_pcal1': 0,
            'f_uim': 1,
            'f_pum': 2,
            'f_tst': 3,
            'f_pcal2': 4,
            'f_pcal3': 5,
            'f_pcal4': 6,
            'f_pcalx_cmp': 7,
            'f_pcaly_cmp': 8,
        }
        freq = np.array(
            [self.calcs.cal_line_sus_pcal_frequency,
             self.calcs.cal_line_sus_uim_frequency,
             self.calcs.cal_line_sus_pum_frequency,
             self.calcs.cal_line_sus_tst_frequency,
             self.calcs.cal_line_sens_pcal_frequency,
             self.calcs.cal_line_high_pcal_frequency,
             self.calcs.cal_line_low_pcal_frequency,
             self.calcs.cal_line_cmp_pcalx_frequency,
             self.calcs.cal_line_cmp_pcaly_frequency,
             ])

        # Build a dictionary for the extra line frequencies
        f_sys = {}
        if hasattr(self.calcs, 'cal_line_sys_pcaly_frequencies'):
            for n, (name, val) in enumerate(self.calcs.cal_line_sys_pcaly_frequencies.items()):
                if name in f_sys.keys():
                    raise ValueError(f'{name} and only be given once in systematic error lines')
                f_sys[name] = val
        if hasattr(self.calcs, 'cal_line_sys_pcalx_frequencies'):
            for n, (name, val) in enumerate(self.calcs.cal_line_sys_pcalx_frequencies.items()):
                if name in f_sys.keys():
                    raise ValueError(f'{name} and only be given once in systematic error lines')
                f_sys[name] = val

        # Add the systematic error lines to the list of frequencies and indicies
        for (name, val) in sorted(f_sys.items()):
            freq_indicies[name] = len(freq_indicies)
            freq = np.append(freq, val)

        assert np.any(freq), ("None of the frequencies can be zero. "
                              f"Please check {freq}")

        R = self.compute_response_function(freq)

        daqdownsampling = daqdownsamplingfilters(2**14, 2**9, 'biquad', 'v3')
        daqdownsampling_response = signal.dfreqresp(daqdownsampling,
                                                    2.0*np.pi*freq/2**14)[1]

        # Pcal corrections
        # See T1700106
        # We are reading the PCAL and DARM signals from the CALCS model, both
        # of which have an implicit 1 16k clock cycle delay. The
        # PCAL_LINE*_CORRECTION is being divided into the DARM/PCAL transfer
        # function (both in CALCS). The compute_pcal_correction uses the
        # "endstation" boolean to indicate that the PCAL channel read is in the
        # CALCS model so it has been divided by a delay.
        # The darm_advance is therefore necessary so that the CALCS DARM signal
        # is properly treated as though it is coming from the OMC model, which
        # is where DARM originates.
        # (DARM / PCAL)_calcs * (1/PCAL_OVER_DARM_LINE*_CORRECTION) =
        #     (DARM_omc / PCAL_end)
        # TODO: the front end and GDS needs to be fixed, and once it is fixed,
        # then this math can be separate EPICS records and be more clear.
        # Meaning, instead of dividing the (DARM/PCAL) transfer function in the
        # front end by PCAL_OVER_DARM_LINE*_CORRECTION, we should multiply.
        # In fact, applying the pcal_correction mutliplied onto the PCAL signal
        # separately from the darm_advance correction multiplied onto the DARM
        # signal before dividing would be even clearer.
        # Once the CALCS and GDS parts are fixed, then we should change this to
        # be DARM_OVER_PCAL_LINE*_CORRECTION = darm_advance / pcal_correction.
        pcal_correction_ref = self.pcal.compute_pcal_correction(
            freq, endstation=gds_pcal_endstation, arm='REF')
        pcal_correction_x = self.pcal.compute_pcal_correction(
            freq, endstation=gds_pcal_endstation, arm='X')
        pcal_correction_y = self.pcal.compute_pcal_correction(
            freq, endstation=gds_pcal_endstation, arm='Y')
        if not gds_darm_omc:
            darm_advance = signal.dfreqresp(
                digital_delay_filter(-1, 16384), 2*np.pi*freq/16384)[1]
        else:
            darm_advance = 1
        PCAL_OVER_DARM_LINE1_CORRECTION = (
            pcal_correction_ref[freq_indicies['f_pcal1']] /
            darm_advance[freq_indicies['f_pcal1']])
        PCAL_OVER_DARM_LINE2_CORRECTION = (
            pcal_correction_ref[freq_indicies['f_pcal2']] /
            darm_advance[freq_indicies['f_pcal2']])
        PCAL_OVER_DARM_LINE3_CORRECTION = (
            pcal_correction_ref[freq_indicies['f_pcal3']] /
            darm_advance[freq_indicies['f_pcal3']])
        PCAL_OVER_DARM_LINE4_CORRECTION = (
            pcal_correction_ref[freq_indicies['f_pcal4']] /
            darm_advance[freq_indicies['f_pcal4']])

        # Compute the same for the systematic error monitor lines but using
        # the correct arm choice
        epics_sys = {}
        for idx, (name, val) in enumerate(f_sys.items()):
            if (hasattr(self.calcs, 'cal_line_sys_pcaly_frequencies') and
                    self.calcs.cal_line_sys_pcaly_frequencies != '' and
                    name in self.calcs.cal_line_sys_pcaly_frequencies):
                epics_sys[f'PCAL_OVER_DARM_{name}_CORRECTION'] = (
                    pcal_correction_y[freq_indicies[name]] / darm_advance[freq_indicies[name]])
            else:
                epics_sys[f'PCAL_OVER_DARM_{name}_CORRECTION'] = (
                    pcal_correction_x[freq_indicies[name]] / darm_advance[freq_indicies[name]])

        PCAL_OVER_DARM_X_COMPARE_CORRECTION = (pcal_correction_x[freq_indicies['f_pcalx_cmp']] /
                                               darm_advance[freq_indicies['f_pcalx_cmp']])
        PCAL_OVER_DARM_Y_COMPARE_CORRECTION = (pcal_correction_y[freq_indicies['f_pcaly_cmp']] /
                                               darm_advance[freq_indicies['f_pcaly_cmp']])

        # For computing EPICS records when gds_pcal_endstation=True, the EPICS
        # are computed as though the channel is at the end station. CALCS will
        # need a phase adjustment in the demods because the channel acquires a
        # phase delay from the model jump to CALCS and the calculation expects
        # no delay (as in GDS).
        # Note that this is POSITIVE because the multiplication is e^(-i*phase)
        # so that positive phase will result in a delay (LHO aLOG 68902)
        if gds_pcal_endstation:
            PCAL_LINE1_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcal1']]/16384), deg=True))
            PCAL_LINE2_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcal2']]/16384), deg=True))
            PCAL_LINE3_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcal3']]/16384), deg=True))
            PCAL_LINE4_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcal4']]/16384), deg=True))

            for idx, (name, val) in enumerate(f_sys.items()):
                epics_sys[f'PCAL_{name}_PCAL_DEMOD_PHASE'] = (
                    np.angle(np.exp(2*np.pi*1j*freq[freq_indicies[name]]/16384), deg=True))

            PCAL_X_COMPARE_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcalx_cmp']]/16384), deg=True))
            PCAL_Y_COMPARE_PCAL_DEMOD_PHASE = (
                np.angle(np.exp(2*np.pi*1j*freq[freq_indicies['f_pcaly_cmp']]/16384), deg=True))
        else:
            PCAL_LINE1_PCAL_DEMOD_PHASE = 0
            PCAL_LINE2_PCAL_DEMOD_PHASE = 0
            PCAL_LINE3_PCAL_DEMOD_PHASE = 0
            PCAL_LINE4_PCAL_DEMOD_PHASE = 0
            for n in np.arange(5, 11):
                epics_sys[f'PCAL_LINE{n}_PCAL_DEMOD_PHASE'] = 0
            PCAL_X_COMPARE_PCAL_DEMOD_PHASE = 0
            PCAL_Y_COMPARE_PCAL_DEMOD_PHASE = 0

        # PCAL over DELTAL_EXTERNAL correction factors are essentially
        # the DTT corrections over PCAL corrections. However, we need the
        # inverse since this value is being divided in the front end.
        # The sign here depends on the arm
        # TODO: in the future this should be fixed in CALCS and GDS so that
        # the correction is multiplicative
        deltal_over_pcal_corr_ref = self.deltal_ext_pcal_correction(
            freq, include_whitening=False, endstation=gds_pcal_endstation,
            arm='REF')
        deltal_over_pcal_corr_x = self.deltal_ext_pcal_correction(
            freq, include_whitening=False, endstation=gds_pcal_endstation,
            arm='X')
        deltal_over_pcal_corr_y = self.deltal_ext_pcal_correction(
            freq, include_whitening=False, endstation=gds_pcal_endstation,
            arm='Y')

        pcal_over_deltal_corr_ref = 1 / deltal_over_pcal_corr_ref
        pcal_over_deltal_corr_x = 1 / deltal_over_pcal_corr_x
        pcal_over_deltal_corr_y = 1 / deltal_over_pcal_corr_y

        PCAL_OVER_DELTAL_LINE1_CORRECTION = pcal_over_deltal_corr_ref[freq_indicies['f_pcal1']]
        PCAL_OVER_DELTAL_LINE2_CORRECTION = pcal_over_deltal_corr_ref[freq_indicies['f_pcal2']]
        PCAL_OVER_DELTAL_LINE3_CORRECTION = pcal_over_deltal_corr_ref[freq_indicies['f_pcal3']]
        PCAL_OVER_DELTAL_LINE4_CORRECTION = pcal_over_deltal_corr_ref[freq_indicies['f_pcal4']]
        for idx, (name, val) in enumerate(f_sys.items()):
            if (hasattr(self.calcs, 'cal_line_sys_pcaly_frequencies') and
                    self.calcs.cal_line_sys_pcaly_frequencies != '' and
                    name in self.calcs.cal_line_sys_pcaly_frequencies):
                epics_sys[f'PCAL_OVER_DELTAL_{name}_CORRECTION'] = (
                    pcal_over_deltal_corr_y[freq_indicies[name]])
            else:
                epics_sys[f'PCAL_OVER_DELTAL_{name}_CORRECTION'] = (
                    pcal_over_deltal_corr_x[freq_indicies[name]])
        PCAL_OVER_DELTAL_X_COMPARE_CORRECTION = (
            pcal_over_deltal_corr_x[freq_indicies['f_pcalx_cmp']])
        PCAL_OVER_DELTAL_Y_COMPARE_CORRECTION = (
            pcal_over_deltal_corr_y[freq_indicies['f_pcaly_cmp']])

        # this does not include any OMC to SUS model jump delay
        uim_actuation_epics = self.actuation.stage_super_actuator_drivealign(
            freq, stage='UIM')
        pum_actuation_epics = self.actuation.stage_super_actuator_drivealign(
            freq, stage='PUM')
        tst_actuation_epics = self.actuation.stage_super_actuator_drivealign(
            freq, stage='TST')

        # super actuator stage
        # this does include OMC to SUS model jump delay
        uim = self.actuation.stage_super_actuator(freq, stage='UIM')
        pum = self.actuation.stage_super_actuator(freq, stage='PUM')
        tst = self.actuation.stage_super_actuator(freq, stage='TST')

        # Actuator EPICS
        # Need to divide out a DAQ downsampling filter from the reference A
        # values because channels sampled at 512 Hz have an AA filter applied
        # See T1700106
        SUS_LINE1_REF_INVA_UIM_RESPRATIO = (
            (1.0 / (uim_actuation_epics[freq_indicies['f_uim']] /
                    daqdownsampling_response[freq_indicies['f_uim']])) *
            (1.0 / R[freq_indicies['f_pcal1']]) * R[freq_indicies['f_uim']])
        SUS_LINE2_REF_INVA_PUM_RESPRATIO = (
            (1.0 / (pum_actuation_epics[freq_indicies['f_pum']] /
                    daqdownsampling_response[freq_indicies['f_pum']])) *
            (1.0 / R[freq_indicies['f_pcal1']]) * R[freq_indicies['f_pum']])
        SUS_LINE3_REF_INVA_TST_RESPRATIO = (
            (1.0 / (tst_actuation_epics[freq_indicies['f_tst']] /
                    daqdownsampling_response[freq_indicies['f_tst']])) *
            (1.0 / R[freq_indicies['f_pcal1']]) * R[freq_indicies['f_tst']])

        # SUS actuation is reading SUS signal sent from the end station
        # (acquires 1 16k clock cycle delay) and the PCAL signal is sent from
        # the end station (also acquiring a 1 clock cycle delay). The PCAL
        # signal is compensated using endstation=False, but not the SUS
        # signal, so we need to include this as an advance (where the CDS
        # demod takes a NEGATIVE phase to induce an advance)
        if gds_sus_endstation:
            SUS_LINE1_SUS_DEMOD_PHASE = (
                np.angle(np.exp(-2*np.pi*1j*freq[freq_indicies['f_uim']]/16384), deg=True))
            SUS_LINE2_SUS_DEMOD_PHASE = (
                np.angle(np.exp(-2*np.pi*1j*freq[freq_indicies['f_pum']]/16384), deg=True))
            SUS_LINE3_SUS_DEMOD_PHASE = (
                np.angle(np.exp(-2*np.pi*1j*freq[freq_indicies['f_tst']]/16384), deg=True))
        else:
            SUS_LINE1_SUS_DEMOD_PHASE = 0
            SUS_LINE2_SUS_DEMOD_PHASE = 0
            SUS_LINE3_SUS_DEMOD_PHASE = 0
            sus_advance = signal.dfreqresp(
                digital_delay_filter(-1, 16384), 2*np.pi*freq/16384)[1]
            SUS_LINE1_REF_INVA_UIM_RESPRATIO *= sus_advance[freq_indicies['f_uim']]
            SUS_LINE2_REF_INVA_PUM_RESPRATIO *= sus_advance[freq_indicies['f_pum']]
            SUS_LINE3_REF_INVA_TST_RESPRATIO *= sus_advance[freq_indicies['f_tst']]

        # Compute the sensing function without the optical response but need to
        # include the optical gain
        coupled_cavity = self.sensing.optical_response(
            self.sensing.coupled_cavity_pole_frequency,
            self.sensing.detuned_spring_frequency,
            self.sensing.detuned_spring_q,
            pro_spring=self.sensing.is_pro_spring)
        sensing_no_cavity_response = (
            self.sensing.compute_sensing(freq) /
            signal.freqresp(coupled_cavity, 2.0*np.pi*freq)[1])
        PCAL_LINE1_REF_C_NOCAVPOLE = sensing_no_cavity_response[freq_indicies['f_pcal1']]
        PCAL_LINE2_REF_C_NOCAVPOLE = sensing_no_cavity_response[freq_indicies['f_pcal2']]

        # DARM digital filtering
        darm_digital_filter_response = self.digital.compute_response(freq)
        PCAL_LINE1_REF_D = darm_digital_filter_response[freq_indicies['f_pcal1']]
        PCAL_LINE2_REF_D = darm_digital_filter_response[freq_indicies['f_pcal2']]

        # Actuation
        PCAL_LINE1_REF_A_UIM = uim[freq_indicies['f_pcal1']]
        PCAL_LINE1_REF_A_PUM = pum[freq_indicies['f_pcal1']]
        PCAL_LINE1_REF_A_TST = tst[freq_indicies['f_pcal1']]
        PCAL_LINE2_REF_A_UIM = uim[freq_indicies['f_pcal2']]
        PCAL_LINE2_REF_A_PUM = pum[freq_indicies['f_pcal2']]
        PCAL_LINE2_REF_A_TST = tst[freq_indicies['f_pcal2']]

        # Output - see T1700106
        out = {
            'CAL-CS_TDEP_PCAL_LINE1_CORRECTION_REAL': PCAL_OVER_DARM_LINE1_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE1_CORRECTION_IMAG': PCAL_OVER_DARM_LINE1_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE1_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_LINE1_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE1_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_LINE1_CORRECTION.imag,
            'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_REAL': SUS_LINE3_REF_INVA_TST_RESPRATIO.real,  # noqa E501
            'CAL-CS_TDEP_SUS_LINE3_REF_INVA_TST_RESPRATIO_IMAG': SUS_LINE3_REF_INVA_TST_RESPRATIO.imag,  # noqa E501
            'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_REAL': SUS_LINE2_REF_INVA_PUM_RESPRATIO.real,  # noqa E501
            'CAL-CS_TDEP_SUS_LINE2_REF_INVA_PUM_RESPRATIO_IMAG': SUS_LINE2_REF_INVA_PUM_RESPRATIO.imag,  # noqa E501
            'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_REAL': SUS_LINE1_REF_INVA_UIM_RESPRATIO.real,  # noqa E501
            'CAL-CS_TDEP_SUS_LINE1_REF_INVA_UIM_RESPRATIO_IMAG': SUS_LINE1_REF_INVA_UIM_RESPRATIO.imag,  # noqa E501
            'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_REAL': PCAL_LINE2_REF_C_NOCAVPOLE.real,
            'CAL-CS_TDEP_PCAL_LINE2_REF_C_NOCAVPOLE_IMAG': PCAL_LINE2_REF_C_NOCAVPOLE.imag,
            'CAL-CS_TDEP_PCAL_LINE2_REF_D_REAL': PCAL_LINE2_REF_D.real,
            'CAL-CS_TDEP_PCAL_LINE2_REF_D_IMAG': PCAL_LINE2_REF_D.imag,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_REAL': PCAL_LINE2_REF_A_TST.real,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_TST_IMAG': PCAL_LINE2_REF_A_TST.imag,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_REAL': PCAL_LINE2_REF_A_PUM.real,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_PUM_IMAG': PCAL_LINE2_REF_A_PUM.imag,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_REAL': PCAL_LINE2_REF_A_UIM.real,
            'CAL-CS_TDEP_PCAL_LINE2_REF_A_UIM_IMAG': PCAL_LINE2_REF_A_UIM.imag,
            'CAL-CS_TDEP_PCAL_LINE2_CORRECTION_REAL': PCAL_OVER_DARM_LINE2_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE2_CORRECTION_IMAG': PCAL_OVER_DARM_LINE2_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE2_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_LINE2_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE2_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_LINE2_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_REAL': PCAL_LINE1_REF_C_NOCAVPOLE.real,
            'CAL-CS_TDEP_PCAL_LINE1_REF_C_NOCAVPOLE_IMAG': PCAL_LINE1_REF_C_NOCAVPOLE.imag,
            'CAL-CS_TDEP_PCAL_LINE1_REF_D_REAL': PCAL_LINE1_REF_D.real,
            'CAL-CS_TDEP_PCAL_LINE1_REF_D_IMAG': PCAL_LINE1_REF_D.imag,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_REAL': PCAL_LINE1_REF_A_TST.real,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_TST_IMAG': PCAL_LINE1_REF_A_TST.imag,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_REAL': PCAL_LINE1_REF_A_PUM.real,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_PUM_IMAG': PCAL_LINE1_REF_A_PUM.imag,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_REAL': PCAL_LINE1_REF_A_UIM.real,
            'CAL-CS_TDEP_PCAL_LINE1_REF_A_UIM_IMAG': PCAL_LINE1_REF_A_UIM.imag,
            'CAL-CS_TDEP_PCAL_LINE3_CORRECTION_REAL': PCAL_OVER_DARM_LINE3_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE3_CORRECTION_IMAG': PCAL_OVER_DARM_LINE3_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE3_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_LINE3_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE3_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_LINE3_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE4_CORRECTION_REAL': PCAL_OVER_DARM_LINE4_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE4_CORRECTION_IMAG': PCAL_OVER_DARM_LINE4_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_LINE4_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_LINE4_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_LINE4_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_LINE4_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_X_COMPARE_CORRECTION_REAL': PCAL_OVER_DARM_X_COMPARE_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_X_COMPARE_CORRECTION_IMAG': PCAL_OVER_DARM_X_COMPARE_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_Y_COMPARE_CORRECTION_REAL': PCAL_OVER_DARM_Y_COMPARE_CORRECTION.real,
            'CAL-CS_TDEP_PCAL_Y_COMPARE_CORRECTION_IMAG': PCAL_OVER_DARM_Y_COMPARE_CORRECTION.imag,
            'CAL-CS_TDEP_PCAL_X_COMPARE_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_X_COMPARE_CORRECTION.real,  # noqa E501
            'CAL-CS_TDEP_PCAL_X_COMPARE_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_X_COMPARE_CORRECTION.imag,  # noqa E501
            'CAL-CS_TDEP_PCAL_Y_COMPARE_DELTAL_PCAL_CORR_REAL': PCAL_OVER_DELTAL_Y_COMPARE_CORRECTION.real,  # noqa E501
            'CAL-CS_TDEP_PCAL_Y_COMPARE_DELTAL_PCAL_CORR_IMAG': PCAL_OVER_DELTAL_Y_COMPARE_CORRECTION.imag,  # noqa E501
            'CAL-CS_TDEP_PCAL_LINE5_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE5_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE5_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE5_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE6_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE6_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE6_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE6_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE7_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE7_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE7_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE7_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE8_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE8_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE8_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE8_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE9_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE9_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE9_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE9_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE10_CORRECTION_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE10_CORRECTION_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE10_DELTAL_PCAL_CORR_REAL': 0,
            'CAL-CS_TDEP_PCAL_LINE10_DELTAL_PCAL_CORR_IMAG': 0,
            'CAL-CS_TDEP_PCAL_LINE1_PCAL_DEMOD_PHASE': PCAL_LINE1_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE2_PCAL_DEMOD_PHASE': PCAL_LINE2_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE3_PCAL_DEMOD_PHASE': PCAL_LINE3_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE4_PCAL_DEMOD_PHASE': PCAL_LINE4_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_LINE5_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_LINE6_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_LINE7_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_LINE8_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_LINE9_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_LINE10_PCAL_DEMOD_PHASE': 0,
            'CAL-CS_TDEP_PCAL_X_COMPARE_PCAL_DEMOD_PHASE': PCAL_X_COMPARE_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_PCAL_Y_COMPARE_PCAL_DEMOD_PHASE': PCAL_Y_COMPARE_PCAL_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE1_SUS_DEMOD_PHASE': SUS_LINE1_SUS_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE2_SUS_DEMOD_PHASE': SUS_LINE2_SUS_DEMOD_PHASE,
            'CAL-CS_TDEP_SUS_LINE3_SUS_DEMOD_PHASE': SUS_LINE3_SUS_DEMOD_PHASE,
        }

        for name in f_sys.keys():
            out[f'CAL-CS_TDEP_PCAL_{name}_CORRECTION_REAL'] = (
                epics_sys[f'PCAL_OVER_DARM_{name}_CORRECTION'].real)
            out[f'CAL-CS_TDEP_PCAL_{name}_CORRECTION_IMAG'] = (
                epics_sys[f'PCAL_OVER_DARM_{name}_CORRECTION'].imag)
            out[f'CAL-CS_TDEP_PCAL_{name}_DELTAL_PCAL_CORR_REAL'] = (
                epics_sys[f'PCAL_OVER_DELTAL_{name}_CORRECTION'].real)
            out[f'CAL-CS_TDEP_PCAL_{name}_DELTAL_PCAL_CORR_IMAG'] = (
                epics_sys[f'PCAL_OVER_DELTAL_{name}_CORRECTION'].imag)
            out[f'CAL-CS_TDEP_PCAL_{name}_PCAL_DEMOD_PHASE'] = (
                epics_sys[f'PCAL_{name}_PCAL_DEMOD_PHASE'])

        if exact:
            # For exact TDCFs (see P2100107, Eqs. 48 - 55)
            PCAL_LINE1_REF_C_NCP_D_A_TST = (
                sensing_no_cavity_response[0] *
                darm_digital_filter_response[0] * tst[0])  # G_{res, T}^1
            PCAL_LINE1_REF_C_NCP_D_A_PUM = (
                sensing_no_cavity_response[0] *
                darm_digital_filter_response[0] * pum[0])  # G_{res, P}^1
            PCAL_LINE1_REF_C_NCP_D_A_UIM = (
                sensing_no_cavity_response[0] *
                darm_digital_filter_response[0] * uim[0])  # G_{res, U}^1
            PCAL_LINE2_REF_C_NCP_D_A_TST = (
                sensing_no_cavity_response[4] *
                darm_digital_filter_response[4] * tst[4])  # G_{res, T}^2
            PCAL_LINE2_REF_C_NCP_D_A_PUM = (
                sensing_no_cavity_response[4] *
                darm_digital_filter_response[4] * pum[4])  # G_{res, P}^2
            PCAL_LINE2_REF_C_NCP_D_A_UIM = (
                sensing_no_cavity_response[4] *
                darm_digital_filter_response[4] * uim[4])  # G_{res, U}^2
            SUS_LINE3_REF_C_NCP_A_TST_NL = (
                sensing_no_cavity_response[3] / daqdownsampling_response[3] *
                tst_actuation_epics[3])  # C_{res}^T A_{T,0}^T
            SUS_LINE3_REF_C_NCP_D_A_TST = (
                sensing_no_cavity_response[3] *
                darm_digital_filter_response[3] * tst[3])  # G_{res, T}^T
            SUS_LINE3_REF_C_NCP_D_A_PUM = (
                sensing_no_cavity_response[3] *
                darm_digital_filter_response[3] * pum[3])  # G_{res, P}^T
            SUS_LINE3_REF_C_NCP_D_A_UIM = (
                sensing_no_cavity_response[3] *
                darm_digital_filter_response[3] * uim[3])  # G_{res, U}^T
            SUS_LINE2_REF_C_NCP_A_PUM_NL = (
                sensing_no_cavity_response[2] / daqdownsampling_response[2] *
                pum_actuation_epics[2])  # C_{res}^P A_{P,0}^P
            SUS_LINE2_REF_C_NCP_D_A_TST = (
                sensing_no_cavity_response[2] *
                darm_digital_filter_response[2] * tst[2])  # G_{res, T}^P
            SUS_LINE2_REF_C_NCP_D_A_PUM = (
                sensing_no_cavity_response[2] *
                darm_digital_filter_response[2] * pum[2])  # G_{res, P}^P
            SUS_LINE2_REF_C_NCP_D_A_UIM = (
                sensing_no_cavity_response[2] *
                darm_digital_filter_response[2] * uim[2])  # G_{res, U}^P
            SUS_LINE1_REF_C_NCP_A_UIM_NL = (
                sensing_no_cavity_response[1] / daqdownsampling_response[1] *
                uim_actuation_epics[1])  # C_{res}^U A_{U,0}^U
            SUS_LINE1_REF_C_NCP_D_A_TST = (
                sensing_no_cavity_response[1] *
                darm_digital_filter_response[1] * tst[1])  # G_{res, T}^U
            SUS_LINE1_REF_C_NCP_D_A_PUM = (
                sensing_no_cavity_response[1] *
                darm_digital_filter_response[1] * pum[1])  # G_{res, P}^U
            SUS_LINE1_REF_C_NCP_D_A_UIM = (
                sensing_no_cavity_response[1] *
                darm_digital_filter_response[1] * uim[1])  # G_{res, U}^U
            PCAL_LINE1_REF_RESP = R[0]  # Eq. 13, R(f_1)
            PCAL_LINE2_REF_RESP = R[4]  # Eq. 13, R(f_2)
            SUS_LINE3_REF_RESP_OVER_A_TST_NL = (
                R[3] / tst_actuation_epics[3] *
                daqdownsampling_response[3])  # Eq. 14, R(f_T) / A_{T,0}(f_T)
            SUS_LINE2_REF_RESP_OVER_A_PUM_NL = (
                R[2] / pum_actuation_epics[2] *
                daqdownsampling_response[2])  # Eq. 14, R(f_P) / A_{P,0}(f_P)
            SUS_LINE1_REF_RESP_OVER_A_UIM_NL = (
                R[1] / uim_actuation_epics[1] *
                daqdownsampling_response[1])  # Eq. 14, R(f_U) / A_{U,0}(f_U)
            SUS_LINE3_REF_A_TST_NL = (
                tst_actuation_epics[3] / daqdownsampling_response[3])  # A_{T,0}(f_T)
            SUS_LINE2_REF_A_PUM_NL = (
                pum_actuation_epics[2] / daqdownsampling_response[2])  # A_{P,0}(f_P)
            SUS_LINE1_REF_A_UIM_NL = (
                uim_actuation_epics[1] / daqdownsampling_response[1])  # A_{U,0}(f_U)

            exact_TDCFs_epics = {
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_TST_REAL':
                    PCAL_LINE1_REF_C_NCP_D_A_TST.real,
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_TST_IMAG':
                    PCAL_LINE1_REF_C_NCP_D_A_TST.imag,
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_PUM_REAL':
                    PCAL_LINE1_REF_C_NCP_D_A_PUM.real,
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_PUM_IMAG':
                    PCAL_LINE1_REF_C_NCP_D_A_PUM.imag,
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_UIM_REAL':
                    PCAL_LINE1_REF_C_NCP_D_A_UIM.real,
                'CAL-CS_TDEP_PCAL_LINE1_REF_C_NCP_D_A_UIM_IMAG':
                    PCAL_LINE1_REF_C_NCP_D_A_UIM.imag,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_TST_REAL':
                    PCAL_LINE2_REF_C_NCP_D_A_TST.real,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_TST_IMAG':
                    PCAL_LINE2_REF_C_NCP_D_A_TST.imag,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_PUM_REAL':
                    PCAL_LINE2_REF_C_NCP_D_A_PUM.real,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_PUM_IMAG':
                    PCAL_LINE2_REF_C_NCP_D_A_PUM.imag,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_UIM_REAL':
                    PCAL_LINE2_REF_C_NCP_D_A_UIM.real,
                'CAL-CS_TDEP_PCAL_LINE2_REF_C_NCP_D_A_UIM_IMAG':
                    PCAL_LINE2_REF_C_NCP_D_A_UIM.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_A_TST_NL_REAL':
                    SUS_LINE3_REF_C_NCP_A_TST_NL.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_A_TST_NL_IMAG':
                    SUS_LINE3_REF_C_NCP_A_TST_NL.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_TST_REAL':
                    SUS_LINE3_REF_C_NCP_D_A_TST.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_TST_IMAG':
                    SUS_LINE3_REF_C_NCP_D_A_TST.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_PUM_REAL':
                    SUS_LINE3_REF_C_NCP_D_A_PUM.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_PUM_IMAG':
                    SUS_LINE3_REF_C_NCP_D_A_PUM.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_UIM_REAL':
                    SUS_LINE3_REF_C_NCP_D_A_UIM.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_C_NCP_D_A_UIM_IMAG':
                    SUS_LINE3_REF_C_NCP_D_A_UIM.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_A_PUM_NL_REAL':
                    SUS_LINE2_REF_C_NCP_A_PUM_NL.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_A_PUM_NL_IMAG':
                    SUS_LINE2_REF_C_NCP_A_PUM_NL.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_TST_REAL':
                    SUS_LINE2_REF_C_NCP_D_A_TST.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_TST_IMAG':
                    SUS_LINE2_REF_C_NCP_D_A_TST.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_PUM_REAL':
                    SUS_LINE2_REF_C_NCP_D_A_PUM.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_PUM_IMAG':
                    SUS_LINE2_REF_C_NCP_D_A_PUM.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_UIM_REAL':
                    SUS_LINE2_REF_C_NCP_D_A_UIM.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_C_NCP_D_A_UIM_IMAG':
                    SUS_LINE2_REF_C_NCP_D_A_UIM.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_A_UIM_NL_REAL':
                    SUS_LINE1_REF_C_NCP_A_UIM_NL.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_A_UIM_NL_IMAG':
                    SUS_LINE1_REF_C_NCP_A_UIM_NL.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_TST_REAL':
                    SUS_LINE1_REF_C_NCP_D_A_TST.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_TST_IMAG':
                    SUS_LINE1_REF_C_NCP_D_A_TST.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_PUM_REAL':
                    SUS_LINE1_REF_C_NCP_D_A_PUM.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_PUM_IMAG':
                    SUS_LINE1_REF_C_NCP_D_A_PUM.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_UIM_REAL':
                    SUS_LINE1_REF_C_NCP_D_A_UIM.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_C_NCP_D_A_UIM_IMAG':
                    SUS_LINE1_REF_C_NCP_D_A_UIM.imag,
                'CAL-CS_TDEP_PCAL_LINE1_REF_RESP_REAL': PCAL_LINE1_REF_RESP.real,
                'CAL-CS_TDEP_PCAL_LINE1_REF_RESP_IMAG': PCAL_LINE1_REF_RESP.imag,
                'CAL-CS_TDEP_PCAL_LINE2_REF_RESP_REAL': PCAL_LINE2_REF_RESP.real,
                'CAL-CS_TDEP_PCAL_LINE2_REF_RESP_IMAG': PCAL_LINE2_REF_RESP.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_RESP_OVER_A_TST_NL_REAL':
                    SUS_LINE3_REF_RESP_OVER_A_TST_NL.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_RESP_OVER_A_TST_NL_IMAG':
                    SUS_LINE3_REF_RESP_OVER_A_TST_NL.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_RESP_OVER_A_PUM_NL_REAL':
                    SUS_LINE2_REF_RESP_OVER_A_PUM_NL.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_RESP_OVER_A_PUM_NL_IMAG':
                    SUS_LINE2_REF_RESP_OVER_A_PUM_NL.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_RESP_OVER_A_UIM_NL_REAL':
                    SUS_LINE1_REF_RESP_OVER_A_UIM_NL.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_RESP_OVER_A_UIM_NL_IMAG':
                    SUS_LINE1_REF_RESP_OVER_A_UIM_NL.imag,
                'CAL-CS_TDEP_SUS_LINE3_REF_A_TST_NL_REAL': SUS_LINE3_REF_A_TST_NL.real,
                'CAL-CS_TDEP_SUS_LINE3_REF_A_TST_NL_IMAG': SUS_LINE3_REF_A_TST_NL.imag,
                'CAL-CS_TDEP_SUS_LINE2_REF_A_PUM_NL_REAL': SUS_LINE2_REF_A_PUM_NL.real,
                'CAL-CS_TDEP_SUS_LINE2_REF_A_PUM_NL_IMAG': SUS_LINE2_REF_A_PUM_NL.imag,
                'CAL-CS_TDEP_SUS_LINE1_REF_A_UIM_NL_REAL': SUS_LINE1_REF_A_UIM_NL.real,
                'CAL-CS_TDEP_SUS_LINE1_REF_A_UIM_NL_IMAG': SUS_LINE1_REF_A_UIM_NL.imag,
            }
            out.update(exact_TDCFs_epics)

        return out
