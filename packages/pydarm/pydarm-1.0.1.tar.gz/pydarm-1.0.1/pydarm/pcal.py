# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.

import numpy as np
from scipy import signal, constants

from .utils import compute_digital_filter_response, digital_delay_filter
from .model import Model


class PcalModel(Model):
    """
    A photon calibrator (pcal) model object

    The class serves to return transfer functions that
    are important to the pcal system, be it corrections
    to the response when pulling the PCAL channels from
    the frames, or establishing force coefficients.

    """

    def __init__(self, config):
        super().__init__(config, measurement='pcal')

        if (not hasattr(self, 'ref_pcal_2_darm_act_sign') and
                hasattr(self, 'ref_pcal')):
            pcalx_sign = getattr(self, 'pcalx_to_darm_act_sign', 1)
            pcaly_sign = getattr(self, 'pcalx_to_darm_act_sign', -1)
            self.ref_pcal_2_darm_act_sign = locals()[
                f'pcal{self.ref_pcal.lower()}_sign']

    def pcal_dewhiten_response(self, frequencies):
        """
        Compute the dewhitening response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the Pcal dewhitening filter

        """

        filt = signal.ZerosPolesGain(
            [], -2.0*np.pi*np.asarray(self.pcal_dewhiten),
            np.prod(-2.0*np.pi*np.asarray(self.pcal_dewhiten)))

        return signal.freqresp(filt, 2.0*np.pi*frequencies)[1]

    def compute_pcal_correction(self, frequencies, endstation=False,
                                include_dewhitening=True, arm='REF'):
        """
        Compute the Pcal correction for the offline analysis
        See G1501518
        NOTE: This also includes the Pcal arm sign, so be aware!

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        endstation : `bool`, optional
            When false (default), the correction is computed for CAL-CS
            PCAL channel, which includes 1 16k clock cycle delay that we must
            compensate (undo). Otherwise, when true, the correction is computed
            at the end station, which does not include 1 16k clock cycle delay
        include_dewhitening : `bool`, optional
            if the dewhitening filter is on (default), then the correction will
            include the two 1 Hz poles
        arm : `str`, optional
            string to indicate which arm is used for this correction, 'REF'
            (default), 'X', or 'Y'

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction

        """

        if arm == 'REF':
            pcal_sign = getattr(self, 'ref_pcal_2_darm_act_sign')
        elif arm == 'X':
            pcal_sign = getattr(self, 'pcalx_to_darm_act_sign', 1)
        elif arm == 'Y':
            pcal_sign = getattr(self, 'pcaly_to_darm_act_sign', -1)
        else:
            raise ValueError(f'arm {arm} is not defined')

        pcal_dewhitening = 1
        if include_dewhitening:
            pcal_dewhitening = self.pcal_dewhiten_response(frequencies)

        pcal_analog_aa = self.analog_aa_or_ai_filter_response(frequencies)
        # As per the Pcal correction factor shown in G1501518, the front end
        # Pcal calibration already takes into account any analog AA gain
        # (if there is any). Therefore, we don't need the analog AA gain
        # to be included in the pcal correction factor
        pcal_analog_aa_hi_f = pcal_analog_aa / \
            np.abs(self.analog_aa_or_ai_filter_response(1e-2))

        pcal_digital_aa = self.digital_aa_or_ai_filter_response(frequencies)

        # Advance filter for end station to CALCS otherwise no delay is used
        # in the correction factor. Remember that the "-1" cycle indicates an
        # advance
        if endstation is False:
            advance_to_bring_pcal_calcs_to_pcal_end = (
                signal.dfreqresp(digital_delay_filter(-1, 2**14),
                                 2.0*np.pi*frequencies/2**14)[1])
        else:
            advance_to_bring_pcal_calcs_to_pcal_end = 1

        return (pcal_sign *
                pcal_dewhitening *
                (1/pcal_analog_aa_hi_f) *
                (1/pcal_digital_aa) *
                advance_to_bring_pcal_calcs_to_pcal_end)

    def digital_filter_response(self, frequencies):
        """
        Importing suspension filter from FOTON file which normalized by whitening
          filter 2 1Hz poles (susnorm) and mpN_DC gain.

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction

        """

        response = np.ones(len(frequencies), dtype='complex128')
        for n in range(len(self.pcal_filter_modules_in_use)):
            if n == 0:
                tf, pfilt = compute_digital_filter_response(
                    self.dpath(self.pcal_filter_file),
                    self.pcal_filter_bank,
                    self.pcal_filter_modules_in_use[n],
                    self.pcal_filter_gain, frequencies, pfilt=None)
            else:
                tf = compute_digital_filter_response(
                    self.dpath(self.pcal_filter_file),
                    self.pcal_filter_bank,
                    self.pcal_filter_modules_in_use[n],
                    self.pcal_filter_gain, frequencies, pfilt=pfilt)[0]
            response *= tf

        return response

    def newtons_per_watt(self):
        """Newtons per watt for the photon calibrator 2*cos(theta)/c"""

        return 2 * np.cos(np.radians(self.pcal_incidence_angle)) / constants.c

    def newtons_per_ct(self, arm='X'):
        """Newtons per count for the photon calibrator"""

        try:
            etm_watts_per_ofs_volt = getattr(
                self, f'pcal{arm.lower()}_etm_watts_per_ofs_volt')
        except AttributeError:
            print(f'Need to specify pcal{arm.lower()}_etm_watts_per_ofs_volt')
            raise

        return (etm_watts_per_ofs_volt *
                self.dac_gain *
                self.newtons_per_watt())

    def hwinj_calibration_newtons_per_ct(self, frequencies, arm='X'):
        """
        Calibration of the hardware injection path, consisting of the photon
        calibrator components: N/ct, corner station to end station analog
        delay (2 16k clock cycles and 4 65k clock cycles), Pcal analog AI,
        and Pcal digital AI.

        Note: this does not include the PCAL to DARM sign

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        arm : `str`, optional
            string to indicate which arm is used for this correction, 'REF'
            'X' (default), or 'Y'

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the correction

        """

        # CS to END, END to IOP, and IOP to analog digital time delays
        # (see G1601472)
        cs_to_end_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        end_to_iop_delay_response = signal.dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        iop_to_analog_delay_response = signal.dfreqresp(
            digital_delay_filter(4, 65536), 2.0*np.pi*frequencies/65536)[1]

        pcal_analog_aa = self.analog_aa_or_ai_filter_response(frequencies)
        # As per the Pcal correction factor shown in G1501518, the front end
        # Pcal calibration already takes into account any analog AA gain
        # (if there is any). Therefore, we don't need the analog AA gain
        # to be included in the pcal correction factor
        pcal_analog_aa_hi_f = pcal_analog_aa / \
            np.abs(self.analog_aa_or_ai_filter_response(1e-2))

        pcal_digital_aa = self.digital_aa_or_ai_filter_response(frequencies)

        tf = (cs_to_end_delay_response *
              end_to_iop_delay_response *
              iop_to_analog_delay_response *
              pcal_analog_aa_hi_f *
              pcal_digital_aa *
              self.newtons_per_ct(arm=arm))

        return tf
