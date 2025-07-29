import pytest
import unittest
import numpy as np
from pydarm.plot import plot, residuals, QuadPlot
from pydarm.darm import DARMModel


CONFIG = '''
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
coupled_cavity_optical_gain = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency = 4.468
detuned_spring_Q = 52.14
sensing_sign = 1
is_pro_spring = True
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1638.001638001638, 1638.001638001638
omc_path_names = A, B
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_gain = 1, 1
omc_meas_z_trans_amplifier_compensated =
omc_meas_p_trans_amplifier_compensated =
omc_meas_z_trans_amplifier_uncompensated =
omc_meas_p_trans_amplifier_uncompensated = 13.7e3, 17.8e3: 13.7e3, 17.8e3

whitening_mode_names = mode1, mode1
omc_meas_z_whitening_compensated_mode1 =
omc_meas_p_whitening_compensated_mode1 =
omc_meas_z_whitening_compensated_mode2 =
omc_meas_p_whitening_compensated_mode2 =
omc_meas_z_whitening_uncompensated_mode1 =
omc_meas_p_whitening_uncompensated_mode1 = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
omc_meas_z_whitening_uncompensated_mode2 =
omc_meas_p_whitening_uncompensated_mode2 =

omc_trans_amplifier_compensation_modules =
omc_whitening_compensation_modules_mode1 =
omc_whitening_compensation_modules_mode2 =
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON
omc_front_end_whitening_compensation_mode2 = ON, ON
omc_filter_noncompensating_modules = 4: 4
adc_clock = 65536

[actuation_x_arm]
darm_feedback_sign = -1
tst_NpV2 = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
suspension_file = test/H1susdata_O3.mat
tst_driver_uncompensated_Z_UL = 129.7e3
tst_driver_uncompensated_Z_LL = 90.74e3
tst_driver_uncompensated_Z_UR = 93.52e3
tst_driver_uncompensated_Z_LR = 131.5e3
tst_driver_uncompensated_P_UL = 3.213e3, 31.5e3
tst_driver_uncompensated_P_LL = 3.177e3, 26.7e3
tst_driver_uncompensated_P_UR = 3.279e3, 26.6e3
tst_driver_uncompensated_P_LR = 3.238e3, 31.6e3
tst_driver_DC_gain_VpV_HV = 40
tst_driver_DC_gain_VpV_LV = 1.881
anti_imaging_rate_string = 16k
anti_imaging_method = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
pum_driver_DC_trans_ApV = 2.6847e-4
pum_coil_outf_signflip = 1
pum_NpA = 0.02947
uim_driver_DC_trans_ApV = 6.1535e-4
uim_NpA = 1.634
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain = 1.0
tst_lock_bank = ETMX_L3_LOCK_L
tst_lock_modules = 5,8,9,10
tst_lock_gain = 1.0
tst_drive_align_bank = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules = 4,5
tst_drive_align_gain = -35.7
pum_lock_bank = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain = 23.0
pum_drive_align_bank = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain = 1.0
uim_lock_bank = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain = 1.06
uim_drive_align_bank = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain = 1.0

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x = OFF, ON, ON, ON
darm_feedback_y = OFF, OFF, OFF, OFF

[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
'''

class TestDarmPlot(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 100)

    def tearDown(self):
        del self.frequencies

    def test_plot(self):
        darm = DARMModel(CONFIG)
        darm.plot(label=['First model'],
                  show=False)


class TestPlotPlot(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 100)

    def tearDown(self):
        del self.frequencies

    def test_plot(self):
        darm = DARMModel(CONFIG)
        test_olg = darm.compute_darm_olg(self.frequencies)
        plot(self.frequencies, test_olg,
             title='Test Plot',
             label=['DARM OLG'],
             show=False)


class TestResiduals(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 100)

    def tearDown(self):
        del self.frequencies

    def test_plot(self):
        measurement = pytest.importorskip("pydarm.measurement")

        meas_object = measurement.Measurement(
            './test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
        meas_freq, meas_tf, meas_coh, meas_unc = meas_object.get_raw_tf(
            'H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_IN1')
        darm = DARMModel(CONFIG)
        test_olg = darm.compute_darm_olg(self.frequencies)
        residuals(self.frequencies, -test_olg,
                  meas_freq, meas_tf, meas_unc,
                  show=False)


class TestQuadPlot(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(1, 4, 100)

    def tearDown(self):
        del self.frequencies

    def test_plot(self):
        darm1 = DARMModel(CONFIG)
        darm2 = darm1
        darm2.sensing.coupled_cavity_pole_frequency = 150
        # Pretend that you have some uncertainty
        fake_uncertainty = np.abs(darm1.compute_darm_olg(self.frequencies))*0.1

        qplot = QuadPlot(title='The Title')
        qplot.plot((self.frequencies, darm1.compute_darm_olg(self.frequencies), fake_uncertainty),
                   (self.frequencies, darm2.compute_darm_olg(self.frequencies)))
        qplot.legend(label=['Test1'])
        qplot.xlim(20, 3000)
        qplot.ylim(1e-10, 1e10, quadrant=['tl'])
        qplot.vlines(300)
        qplot.text(200, 2, 'testing')
        qplot.xscale()
        qplot.yscale()


if __name__ == '__main__':
    unittest.main()
