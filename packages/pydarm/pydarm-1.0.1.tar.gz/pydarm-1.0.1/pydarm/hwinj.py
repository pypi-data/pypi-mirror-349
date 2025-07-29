# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#
# This file is part of pyDARM.

from .model import Model
from .pcal import PcalModel
from .actuation import DARMActuationModel
from .sensing import SensingModel
from .utils import write_hwinj_data


class HwinjModel(Model):

    def __init__(self, config):
        super().__init__(config)

        self.actuation = DARMActuationModel(config)
        self.pcal = PcalModel(config)
        self.sensing = SensingModel(config)

    def hwinj_pcal_actuation(self, frequencies, arm='X'):
        """
        Calibration of the hardware injection path, consisting of the photon
        calibrator components: sign, N/ct, corner station to end station analog
        delay (2 16k clock cycles and 4 65k clock cycles), Pcal analog AI,
        and Pcal digital AI; dynamical response of the arm TST mass; and
        meters to strain from sensing

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

        if arm == 'REF':
            pcal_sign = getattr(self, 'ref_pcal_2_darm_act_sign')
        elif arm == 'X':
            pcal_sign = getattr(self, 'pcalx_to_darm_act_sign', 1)
        elif arm == 'Y':
            pcal_sign = getattr(self, 'pcaly_to_darm_act_sign', -1)
        else:
            raise ValueError(f'arm {arm} is not defined')

        pcal_newtons_per_ct = self.pcal.hwinj_calibration_newtons_per_ct(
            frequencies, arm=arm)

        if arm == 'X':
            sus_m_per_newton = self.actuation.xarm.matlab_force2length_response(
                self.dpath(self.actuation.xarm.suspension_file), frequencies)[2]
        elif arm == 'Y':
            sus_m_per_newton = self.actuation.yarm.matlab_force2length_response(
                self.dpath(self.actuation.yarm.suspension_file), frequencies)[2]
        else:
            raise ValueError("arm must be 'X' or 'Y'")

        meters_to_strain = 1 / self.sensing.mean_arm_length()

        tf = (pcal_sign *
              pcal_newtons_per_ct *
              sus_m_per_newton *
              meters_to_strain)

        return tf

    def save_hwinj_pcal_actuation(self, frequencies, save_to_file, arm='X',
                                  name='', info=''):
        """Write an ASCII file for the hardware injection transfer function

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies for the transfer function
        save_to_file : str
            Output filename
        arm : `str`, optional
            string to indicate which arm is used for this correction, 'REF'
            'X' (default), or 'Y'
        name : `str`, optional
            Optional extra name string printed to the header
        info : `str`, optional
            Optional additional information string printed to the header

        """

        tf = self.hwinj_pcal_actuation(frequencies, arm=arm)

        write_hwinj_data(frequencies, tf, filename=save_to_file, name=name, info=info)
