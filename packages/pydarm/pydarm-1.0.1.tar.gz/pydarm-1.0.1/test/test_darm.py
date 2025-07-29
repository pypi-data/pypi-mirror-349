import unittest
import pydarm
import numpy as np


class TestComputeDigitalFilterResponse(unittest.TestCase):

    def setUp(self):
        # frequencies = np.logspace(0, np.log10(5000.), 10)
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_digital_filter_response = np.array(
            [-3513076500191.6504+3327250871150.924j,
             -164538201540.2522+209970221596.44916j,
             -3242877524.3140893-646390346.0757524j,
             3152750901.033689+60862553.6703552j,
             5968957387.406848+6106710482.173726j,
             17063001608.677845+14901038698.213606j,
             59173157596.065796-25364518140.6575j,
             -46407563930.73129+21858627480.823456j,
             -9021881.73649469-6742239.626013521j,
             -27770965.672582164+52593450.2554684j])

    def tearDown(self):
        del self.frequencies
        del self.known_digital_filter_response

    def test_compute_digital_filter_response(self):
        """ Test the DARM digital filter repsonse """
        D = pydarm.darm.DigitalModel('''
[digital]
digital_filter_file = test/H1OMC_1239468752.txt
digital_filter_bank = LSC_DARM1, LSC_DARM2
digital_filter_modules = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain = 400,1
''')
        test_response = D.compute_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            # Requires investigation why this delta tolerance has to be higher
            # on some systems in order to pass.
            # Can test using print() to check output and call test using
            # pytest -s test/darm_test.py
            self.assertAlmostEqual(
                np.abs(test_response[n]) /
                np.abs(self.known_digital_filter_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_digital_filter_response[n], deg=True), 0.0,
                places=5)


class TestComputeDarm(unittest.TestCase):

    def setUp(self):
        self.config = '''
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
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_uncompensated_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1638.001638001638, 1638.001638001638
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules = 4: 4
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_test = ON, ON
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
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_olg = np.array(
            [-346589.7289879694+67697.98179370671j,
             -1859.4410636292505+7152.898242047175j,
             40.79712693912431-10.496083469022562j,
             -3.200667505597764+0.6749176141222187j,
             -1.0964382128049217-0.6352470027806889j,
             -0.48849524504067693-0.12453097698086546j,
             0.07580387098963454+0.20189845660408226j,
             -0.010730361938738586+0.010017089450759862j,
             1.1367097388995271e-07-1.7573024415341907e-07j,
             -1.8569508267009735e-08+2.419265648650538e-08j])
        self.known_response = np.array(
            [2.0406181004597967-0.4013213677915312j,
             0.0011220990463462926-0.004469979302356652j,
             7.174381300234404e-06-1.4617952572908577e-06j,
             -6.479990333472527e-07+1.5653156901534748e-07j,
             -1.3662040618868035e-09-1.9861756619000937e-07j,
             1.6810351811864666e-07+2.0548446256238736e-08j,
             2.1237360469410807e-07+3.590194203666282e-07j,
             -7.07952406495893e-08+6.371681259820066e-07j,
             -1.4643321723110076e-06+3.0336488559992614e-07j,
             4.465169869308327e-06-1.5260050031500522e-06j])

    def tearDown(self):
        del self.config
        del self.frequencies
        del self.known_olg
        del self.known_response

    def test_compute_darm_olg(self):
        """ Test DARM open loop gain response """
        darm = pydarm.darm.DARMModel(self.config)
        test_olg = darm.compute_darm_olg(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_olg[n]) / np.abs(self.known_olg[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_olg[n], deg=True) -
                np.angle(self.known_olg[n], deg=True), 0.0, places=5)

    def test_compute_darm_response_function(self):
        """ Test DARM closed loop response function """
        darm = pydarm.darm.DARMModel(self.config)
        test_response = darm.compute_response_function(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)


class TestComputeEtas(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(np.log10(20), np.log10(2000), 10)
        self.syserr_input = np.array(
            [1.0000003831992847-0.0007929858798234665j,
             0.9999986255804106-0.002042969515282433j,
             0.9999869597043107-0.0052632862823899385j,
             0.9999095302557972-0.013559488366496989j,
             0.9993956411093269-0.03492779907418393j,
             0.995986356934377-0.08988999137528689j,
             0.9734269429695694-0.22996802633705743j,
             0.8267642616923517-0.5649608162253222j,
             -0.004181642663901519-1.003311656263212j,
             -0.19691508479464048+0.7796521952236531j])
        self.known_etas = np.array(
            [[0.99997492-4.43808402e-04j, 0.99816941-1.32625955e-03j,
              0.99042173+2.75217421e-03j, 0.98764461+2.40563425e-02j,
              1.00478583+5.90395517e-02j, 1.01828258+8.71417774e-02j,
              0.94939253+2.12468056e-01j, 0.82362819+5.75180328e-01j,
              -0.00435558+9.98282271e-01j, -0.30462374-1.20565509e+00j],
             [1.-0.00000000e+00j, 1.-0.00000000e+00j,
              1.-0.00000000e+00j, 1.+0.00000000e+00j,
              1.+0.00000000e+00j, 1.-6.08247505e-17j,
              1.+0.00000000e+00j, 1.+0.00000000e+00j,
              1.+0.00000000e+00j, 1.-0.00000000e+00j],
             [0.99997492-4.43808402e-04j, 0.99816941-1.32625955e-03j,
              0.99042173+2.75217421e-03j, 0.98764461+2.40563425e-02j,
              1.00478583+5.90395517e-02j, 1.01828258+8.71417774e-02j,
              0.94939253+2.12468056e-01j, 0.82362819+5.75180328e-01j,
              -0.00435558+9.98282271e-01j, -0.30462374-1.20565509e+00j]])

    def tearDown(self):
        del self.frequencies
        del self.syserr_input
        del self.known_etas

    def test_compute_etas(self):
        model_string = '''
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
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
whitening_mode_names = test, test
omc_meas_p_whitening_uncompensated_test   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_test = ON, ON
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
        darm = pydarm.darm.DARMModel(model_string)
        test_eta_R_c, test_eta_R_a, test_eta_R = \
            darm.compute_etas(self.frequencies, sensing_syserr=self.syserr_input)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_eta_R_c[n]) / np.abs(self.known_etas[0][n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_eta_R_c[n], deg=True) -
                np.angle(self.known_etas[0][n], deg=True), 0.0, places=5)
            self.assertAlmostEqual(
                np.abs(test_eta_R_a[n]) / np.abs(self.known_etas[1][n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_eta_R_a[n], deg=True) -
                np.angle(self.known_etas[1][n], deg=True), 0.0, places=5)
            self.assertAlmostEqual(
                np.abs(test_eta_R[n]) / np.abs(self.known_etas[2][n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_eta_R[n], deg=True) -
                np.angle(self.known_etas[2][n], deg=True), 0.0, places=5)


if __name__ == '__main__':
    unittest.main()
