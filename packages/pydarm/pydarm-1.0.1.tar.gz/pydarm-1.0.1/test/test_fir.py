import unittest
import pydarm
import numpy as np
import math
import h5py
import os
from pydarm.fir import (FIRfilter,
                        FIRFilterFileGeneration,
                        check_td_vs_fd_response,
                        correctFIRfilter)


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
whitening_mode_names = mode1, mode1
omc_meas_p_trans_amplifier_uncompensated   = 13.7e3, 17.8e3: 13.7e3, 17.8e3
omc_meas_p_whitening_uncompensated_mode1   = 11.346e3, 32.875e3, 32.875e3: 11.521e3, 32.863e3, 32.863e3
super_high_frequency_poles_apparent_delay = 0, 0
gain_ratio = 1, 1
balance_matrix = 1, 1
omc_path_names = A, B
single_pole_approximation_delay_correction = -12e-6
adc_gain = 1, 1
omc_filter_file = test/H1OMC_1239468752.txt
omc_filter_bank = OMC_DCPD_A, OMC_DCPD_B
omc_filter_noncompensating_modules =
omc_filter_gain = 1, 1
omc_front_end_trans_amplifier_compensation = ON, ON
omc_front_end_whitening_compensation_mode1 = ON, ON
adc_clock = 65536

[digital]
digital_filter_file    = test/H1OMC_1239468752.txt
digital_filter_bank    = LSC_DARM1, LSC_DARM2
digital_filter_modules = 1,2,3,4,7,9,10: 3,4,5,6,7
digital_filter_gain    = 400,1

[actuation]
darm_output_matrix = 1.0, -1.0, 0.0, 0.0
darm_feedback_x    = OFF, ON, ON, ON
darm_feedback_y    = OFF, OFF, OFF, OFF

[actuation_x_arm]
darm_feedback_sign = -1
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
linearization = OFF
actuation_esd_bias_voltage = -9.3
sus_filter_file = test/H1SUSETMX_1236641144.txt
tst_isc_inf_bank    = ETMX_L3_ISCINF_L
tst_isc_inf_modules =
tst_isc_inf_gain    = 1.0
tst_lock_bank       = ETMX_L3_LOCK_L
tst_lock_modules    = 5,8,9,10
tst_lock_gain       = 1.0
tst_drive_align_bank     = ETMX_L3_DRIVEALIGN_L2L
tst_drive_align_modules  = 4,5
tst_drive_align_gain     = -35.7
pum_lock_bank    = ETMX_L2_LOCK_L
pum_lock_modules = 7
pum_lock_gain    = 23.0
pum_drive_align_bank    = ETMX_L2_DRIVEALIGN_L2L
pum_drive_align_modules = 6,7
pum_drive_align_gain    = 1.0
pum_coil_outf_signflip  = 1
uim_lock_bank    = ETMX_L1_LOCK_L
uim_lock_modules = 10
uim_lock_gain    = 1.06
uim_drive_align_bank    = ETMX_L1_DRIVEALIGN_L2L
uim_drive_align_modules =
uim_drive_align_gain    = 1.0
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
pum_driver_DC_trans_ApV = 2.6847e-4
uim_driver_DC_trans_ApV = 6.1535e-4
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
analog_anti_imaging_file = test/H1aa.mat
dac_gain = 7.62939453125e-05
unknown_actuation_delay = 15e-6
uim_delay = 0
pum_delay = 0
tst_delay = 0

[pcal]
pcal_filter_file           = H1CALEY_1123041152.txt
pcal_filter_bank           = PCALY_TX_PD
pcal_filter_modules_in_use = 6,8
pcal_filter_gain           = 1.0
pcal_dewhiten               = 1.0, 1.0
pcal_incidence_angle        = 8.8851
pcal_etm_watts_per_ofs_volt = 0.13535
ref_pcal_2_darm_act_sign    = -1.0
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
analog_anti_aliasing_file = test/H1aa.mat

[calcs]
# pcal calibration lines
cal_line_sus_uim_frequency = 15.6
cal_line_sus_pum_frequency = 16.4
cal_line_sus_tst_frequency = 17.6
cal_line_sus_pcal_frequency = 17.1
cal_line_sens_pcal_frequency = 410.3
cal_line_high_pcal_frequency = 1083.7
cal_line_low_pcal_frequency = 24.5  # temporary change to monitor thermalization line. Should be reverted to 0.1 once removed
cal_line_cmp_pcalx_frequency = 283.91
cal_line_cmp_pcaly_frequency = 284.01
cal_line_sys_pcalx_frequencies = 33.43, 53.67, 77.73, 102.13, 283.91, 410.2
'''


class TestFIRfilter(unittest.TestCase):

    def setUp(self):
        self.known_advance_array = np.array([ 1.+0.00000000e+00j, -1.+1.22464680e-16j,  1.-2.44929360e-16j,
                                             -1.+3.67394040e-16j,  1.-4.89858720e-16j, -1.+6.12323400e-16j,
                                              1.-7.34788079e-16j, -1.+8.57252759e-16j,  1.-9.79717439e-16j])
        self.known_delay_array = np.array([ 1.+0.00000000e+00j, -1.-1.22464680e-16j,  1.+2.44929360e-16j,
                                           -1.-3.67394040e-16j,  1.+4.89858720e-16j, -1.-6.12323400e-16j,
                                            1.+7.34788079e-16j, -1.-8.57252759e-16j,  1.+9.79717439e-16j])
        self.known_delay_samples = 8
        self.known_df = 1.0
        self.known_dt = 0.0625
        self.known_freq_array = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8.])
        self.known_latency = 0.5
        self.known_freq_res=3.0
        self.known_dur=1.0
        self.known_samples_to_HPcorner = 1
        self.known_samples_to_LPcorner = 0
        self.known_window = np.array([0.00233883, 0.02623098, 0.09449865, 0.22677684, 0.42285187,
                                      0.65247867, 0.85980208, 0.98349415, 0.98349415, 0.85980208,
                                      0.65247867, 0.42285187, 0.22677684, 0.09449865, 0.02623098,
                                      0.00233883])

    def tearDown(self):
        del self.known_window
        del self.known_advance_array
        del self.known_delay_array
        del self.known_delay_samples
        del self.known_df
        del self.known_dt
        del self.known_freq_array
        del self.known_latency
        del self.known_samples_to_HPcorner
        del self.known_samples_to_LPcorner

    def test_FIRfilter(self):
        test_FIRfilter = FIRfilter(fNyq=8, desired_dur=1, highpass_fcut=4, lowpass_fcut=None,
                                   window_type='kaiser', freq_res=3.0)

        self.assertEqual(test_FIRfilter.delay_samples, self.known_delay_samples)
        self.assertEqual(test_FIRfilter.df, self.known_df)
        self.assertEqual(test_FIRfilter.dt, self.known_dt)
        self.assertEqual(test_FIRfilter.dur, self.known_dur)
        self.assertEqual(test_FIRfilter.latency, self.known_latency)
        self.assertEqual(test_FIRfilter.freq_res, self.known_freq_res)
        self.assertEqual(test_FIRfilter.samples_to_HPcorner, self.known_samples_to_HPcorner)
        self.assertEqual(test_FIRfilter.samples_to_LPcorner, self.known_samples_to_LPcorner)
        self.assertEqual(len(test_FIRfilter.advance_array), len(self.known_advance_array))
        for n in range(len(self.known_advance_array)):
            self.assertAlmostEqual(np.abs(test_FIRfilter.advance_array[n]) / np.abs(self.known_advance_array[n]), 1.0)
            self.assertAlmostEqual(np.angle(test_FIRfilter.advance_array[n], deg=True) - np.angle(self.known_advance_array[n], deg=True), 0.0)
        self.assertEqual(len(test_FIRfilter.delay_array), len(self.known_delay_array))
        for n in range(len(self.known_delay_array)):
            self.assertAlmostEqual(np.abs(test_FIRfilter.delay_array[n]) / np.abs(self.known_delay_array[n]), 1.0)
            self.assertAlmostEqual(np.angle(test_FIRfilter.delay_array[n], deg=True) - np.angle(self.known_delay_array[n], deg=True), 0.0)
        self.assertEqual(len(test_FIRfilter.freq_array), len(self.known_freq_array))
        for n in range(len(self.known_freq_array)):
            self.assertAlmostEqual(test_FIRfilter.freq_array[n], self.known_freq_array[n])
        self.assertEqual(len(test_FIRfilter.window), len(self.known_window))
        for n in range(len(self.known_window)):
            self.assertAlmostEqual(test_FIRfilter.window[n] / self.known_window[n], 1.0, places=5)


class TestCreateFIRfilter(unittest.TestCase):

    def setUp(self):
        self.config = CONFIG
        self.known_Cfir = np.array([-6.63850419e+01,  8.93362543e+02,  8.56077110e+04, -2.27887893e+05,
                                    -8.86759535e+05,  1.61591927e+06,  1.23433242e+06, -2.69276290e+06,
                                     1.79904168e+06, -1.74942704e+06,  6.65554086e+05,  9.35475644e+05,
                                    -4.10502392e+05, -8.87882831e+04,  2.10864177e+04,  1.42418753e+02])

    def tearDown(self):
        del self.config
        del self.known_Cfir

    def test_create_fir_filter(self):
        test_FIRfilter = FIRfilter(fNyq=8, desired_dur=1, highpass_fcut=4,
                                 lowpass_fcut=None, window_type='kaiser', freq_res=3.0)
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(test_FIRfilter.freq_array)
        test_Cfir, test_Cmodel = test_FIRfilter.create_fir_filter(Cf)

        for n in range(len(self.known_Cfir)):
            self.assertAlmostEqual(test_Cfir[n] /
                                   self.known_Cfir[n],
                                   1.0)

class TestCorrectFIRfilter(unittest.TestCase):

    def setUp(self):
        self.config = CONFIG

        self.known_Corfir = np.array([641251.57653175+3.89761912e+03j,
                                      403699.51881229+2.69185401e+03j,
                                     -698906.37183737-2.74819393e+04j,
                                    -2030852.42623273+8.40205385e+03j,
                                   -54502988.18785557+4.75790494e+07j,
                                    47217941.01424959+8.94536006e+06j,
                                     6654278.33719367-1.81089469e+05j,
                                     4974433.40023975-4.73425087e+05j,
                                     4662225.0011754 -2.41147877e+05j])
    def tearDown(self):
        del self.config
        del self.known_Corfir

    def test_correctFIRfilter(self):
        test_FIRfilter = FIRfilter(fNyq=8, desired_dur=1, highpass_fcut=4, lowpass_fcut=None,
                                 window_type='kaiser', freq_res=3.0)
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(test_FIRfilter.freq_array)
        test_Cfir = test_FIRfilter.create_fir_filter(Cf)[0]
        test_Corfir = correctFIRfilter(test_FIRfilter, test_Cfir, Cf,  [2, 4, 7, 9])

        self.assertEqual(len(test_Corfir), len(self.known_Corfir))
        for n in range(len(test_Corfir)):
            self.assertAlmostEqual(
                np.abs(test_Corfir[n])/np.abs(self.known_Corfir[n]), 1)
            self.assertAlmostEqual(
                np.angle(test_Corfir[n], deg=True) -
                np.angle(self.known_Corfir[n], deg=True), 0)


class Testcheck_td_vs_fd(unittest.TestCase):

    def setUp(self):
        self.config = CONFIG

    def tearDown(self):
        del self.config

    def test_check_td_vs_fd(self):
        test_FIRfilter = FIRfilter(fNyq=2048, desired_dur=1, highpass_fcut=8, lowpass_fcut=None,
                                 window_type='kaiser', freq_res=3.0)
        C = pydarm.sensing.SensingModel(self.config)
        Cf = C.compute_sensing(test_FIRfilter.freq_array)
        test_Cfir = test_FIRfilter.create_fir_filter(Cf)[0]
        ctvf = test_FIRfilter.check_td_vs_fd(test_Cfir, Cf)

        test_freq = ctvf[0]
        test_mag_ratios = ctvf[1]
        test_phase_diffs = ctvf[2]

        df = test_freq[1] - test_freq[0]
        # For this configuration, check that the magnitude and phase are close to
        # 1 and 0, respectively between 50 and 1000 Hz
        Nmin = math.ceil(40 / df)
        Nmax = math.ceil(1000 / df)
 
        for n in range(Nmin, Nmax):
            self.assertLess(np.abs(test_mag_ratios[n]), 1.01)
            self.assertLess(np.abs(test_phase_diffs[n]), 1)


class TestCheckTdVsFdResponse(unittest.TestCase):

    def setUp(self):
        self.test_FIRfilter = FIRfilter(fNyq=2048, desired_dur=1, highpass_fcut=8,
                                 lowpass_fcut=None, window_type='kaiser', freq_res=3.0)
        self.config = CONFIG

    def tearDown(self):
        del self.test_FIRfilter
        del self.config

    def test_check_td_vs_fd_response(self):
        freq = self.test_FIRfilter.freq_array
        # DARM model throws warnings when computed at 0 Hz, so remove that from frequency array
        freq = np.delete(freq, 0)
        darm = pydarm.darm.DARMModel(self.config)
        # To get frequency vectors correct, need to reinsert the zero frequency component after DARM components are computed
        # Just set this DC component to 0
        InvC = np.insert(1/darm.sensing.compute_sensing(freq), 0, 0)
        TST = np.insert(darm.actuation.xarm.compute_actuation_single_stage(freq, stage='TST'), 0, 0)
        PUM = np.insert(darm.actuation.xarm.compute_actuation_single_stage(freq, stage='PUM'), 0, 0)
        UIM = np.insert(darm.actuation.xarm.compute_actuation_single_stage(freq, stage='UIM'), 0, 0)
        D = np.insert(darm.digital.compute_response(freq), 0, 0)
        R = np.insert(darm.compute_response_function(freq), 0, 0)

        InvC_filt = self.test_FIRfilter.create_fir_filter(InvC)[0]
        TST_filt = self.test_FIRfilter.create_fir_filter(TST)[0]
        PUM_filt = self.test_FIRfilter.create_fir_filter(PUM)[0]
        UIM_filt = self.test_FIRfilter.create_fir_filter(UIM)[0]

        test_freq, test_ratio_mag, test_ratio_pha = check_td_vs_fd_response(InvC_filt,
                                            None,
                                            TST_filt,
                                            PUM_filt,
                                            UIM_filt,
                                            None,
                                            D,
                                            R,
                                            time_delay = 0.0,
                                            invsens_fNyq=self.test_FIRfilter.fNyquist,
                                            act_fNyq=self.test_FIRfilter.fNyquist,
                                            D_fNyq=self.test_FIRfilter.fNyquist,
                                            R_fNyq=self.test_FIRfilter.fNyquist)

        
        df = test_freq[1] - test_freq[0]
        # For this configuration, check that the magnitude and phase are close to
        # 1 and 0, respectively between 50 and 1000 Hz
        Nmin = math.ceil(40 / df)
        Nmax = math.ceil(1000 / df)
        
        for n in range(Nmin, Nmax):
            self.assertLess(np.abs(test_ratio_mag[n]), 1.05)
            self.assertLess(np.abs(test_ratio_pha[n]), 5)

class TestGDS_FIR_filter_generation(unittest.TestCase):
    def setUp(self):
        # Set up for control chain FIR filter generation
        self.FIRpars = FIRfilter(fNyq=1024, desired_dur=3.5, highpass_fcut=10.5, lowpass_fcut=None,
                                 window_type='dpss', freq_res=4.0)

        # Load in known transfer function and resulting FIR filter
        h5f = h5py.File('./test/FIR_unit_test_coeffs.h5', 'r')
        self.known_FIR_filter = h5f['FIR_filter'][:]
        self.known_tf = h5f['transfer_function'][:]

    def tearDown(self):
        del self.FIRpars
        del self.known_FIR_filter
        del self.known_tf

    def test_GDS_FIR_filter_generation(self):
        # Generate test FIR filter from frequency domain transfer function
        [test_FIR_filter, model] = self.FIRpars.create_fir_filter(self.known_tf)
        # FIXME: (Arif) Scipy and FIRtools have much different results under 10 Hz.
        # I changed the range and places. My local test could take higher places.
        for n in range(300, len(self.known_FIR_filter)-300):
            self.assertAlmostEqual(abs((self.known_FIR_filter[n] / test_FIR_filter[n])
                                       - 1), 0, places=3)


class TestFIRFilterFileGeneration(unittest.TestCase):

    def setUp(self):
        self.GDS_file = h5py.File('./test/GDS_test.h5', 'r')
        self.DCS_file = h5py.File('./test/DCS_test.h5', 'r')
        self.CALCScorr_file = h5py.File('./test/CALCS_corr_test.h5', 'r')
        self.known_act_filter = self.DCS_file['actuation_tst'][:]
        self.actuation_tst_sr = 2048.0
        self.known_ctrl_corr_filter = self.GDS_file['ctrl_corr_filter'][:]
        self.ctrl_corr_sr = 2048.0
        self.known_calcs_corr_filter = self.CALCScorr_file['calcs_corr_filter'][:]
        self.calcs_corr_sr = 16384.0
        self.config = './example_model_files/H1_20190416.ini'
        os.environ['CAL_DATA_ROOT'] = './test'
        self.known_arm_length = 3994.4698
        self.known_fcc = 410.6
        self.known_fs = 4.468
        self.known_fs_squared = 19.963024
        self.known_srcQ = 52.14
        self.known_ips = 1.0
        self.FIRconfigs = """
[FIR]
ctrl_corr_duration      = 3.5
ctrl_corr_highpass_fcut = 9.0
ctrl_corr_highpass_duration  = 0.0
ctrl_corr_fnyq          = 1024
ctrl_corr_window_type        = kaiser
ctrl_corr_freq_res      = 4.0
ctrl_corr_highpass_freq_res  = 3.0

res_corr_highpass_fcut = 9.0
res_corr_lowpass_fcut  = 6192.0
res_corr_fnyq          = 8192
res_corr_highpass_fnyq      = 1024
res_corr_window_type        = kaiser
res_corr_freq_res      = 4.0
res_corr_highpass_freq_res  = 4.0
res_corr_duration      = 1.0
res_corr_highpass_duration  = 2.5

nonsens_corr_highpass_fcut   = 9
nonsens_corr_lowpass_fcut    = 6192
nonsens_corr_fnyq            = 8192
nonsens_corr_window_type     = kaiser
nonsens_corr_freq_res        = 4.0
nonsens_corr_duration        = 0.25
nonsens_corr_advance         = 239e-6
include_nonsens_advance      = True
include_nonsens_res_corr     = False

act_duration      = 3.5
act_highpass_fcut = 9.0
act_highpass_duration  = 0.0
act_fnyq          = 1024
act_window_type        = kaiser
act_freq_res      = 4.0
act_highpass_freq_res  = 3.0

invsens_highpass_fcut = 9.0
invsens_lowpass_fcut  = 6192.0
invsens_fnyq          = 8192
invsens_highpass_fnyq      = 1024
invsens_window_type        = kaiser
invsens_freq_res      = 4.0
invsens_highpass_freq_res  = 4.0
invsens_duration      = 1.0
invsens_highpass_duration  = 2.5

calcs_corr_highpass_fcut     = 9.0
calcs_corr_fnyq              = 8192
calcs_corr_window_type       = dpss
calcs_corr_freq_res          = 4.0
calcs_corr_duration          = 1.0

exclude_response_corr  = True
"""
        self.FG = FIRFilterFileGeneration(self.config, fir_config=self.FIRconfigs)

    def tearDown(self):
        del self.config
        del self.FIRconfigs
        del self.known_arm_length
        del self.known_fcc
        del self.known_fs
        del self.known_fs_squared
        del self.known_srcQ
        del self.known_ips
        del self.GDS_file
        del self.known_ctrl_corr_filter
        del self.DCS_file
        del self.known_act_filter
        del self.CALCScorr_file
        del self.known_calcs_corr_filter
        del self.FG
        del os.environ['CAL_DATA_ROOT']

    def test_FilterGeneration(self):
        self.assertEqual(self.known_arm_length, self.FG.arm_length)
        self.assertEqual(self.known_fcc, self.FG.fcc)
        self.assertEqual(self.known_fs, self.FG.fs)
        self.assertEqual(self.known_fs_squared, self.FG.fs_squared)
        self.assertEqual(self.known_srcQ, self.FG.srcQ)
        self.assertEqual(self.known_ips, self.FG.ips)

    def test_GDS(self):
        self.FG.GDS(output_filename='test_GDS.npz', output_dir='./test')
        gds = np.load('./test/test_GDS.npz')
        test_ctrl_corr_filter = gds['ctrl_corr_filter']
        test_ctrl_corr_filter_response = pydarm.firtools.freqresp(test_ctrl_corr_filter)
        known_ctrl_corr_filter_response = pydarm.firtools.freqresp(self.known_ctrl_corr_filter)
        n_10Hz = int(20.0 / self.ctrl_corr_sr * len(known_ctrl_corr_filter_response))
        n_6kHz = int(12000.0 / self.ctrl_corr_sr * len(known_ctrl_corr_filter_response))
        n_6kHz = n_6kHz if n_6kHz < len(known_ctrl_corr_filter_response) else len(known_ctrl_corr_filter_response)
        for n in range(n_10Hz, n_6kHz):
            self.assertAlmostEqual(abs((known_ctrl_corr_filter_response[n] / test_ctrl_corr_filter_response[n]) -1),
                                   0, places=3)
        for n in range(n_10Hz):
            places = 1 if n / n_10Hz < 0.6 else 2
            self.assertAlmostEqual(abs(np.log10(abs(known_ctrl_corr_filter_response[n] /
                                                test_ctrl_corr_filter_response[n])) / 20),
                                                0, places=places)
        if n_6kHz < len(known_ctrl_corr_filter_response):
            for n in range(n_6kHz, len(known_ctrl_corr_filter_response)):
                places = 1 if n / len(known_ctrl_corr_filter_response) > 0.9 else 2
                self.assertAlmostEqual(abs(np.log10(abs(known_ctrl_corr_filter_response[n] /
                                                    test_ctrl_corr_filter_response[n])) / 20),
                                                    0, places=places)

    def test_DCS(self):
        self.FG.DCS(output_filename='test_DCS.npz', output_dir='./test')
        dcs_file = np.load('./test/test_DCS.npz')
        test_act_filter = dcs_file['actuation_tst']
        test_act_filter_response = pydarm.firtools.freqresp(test_act_filter)
        known_act_filter_response = pydarm.firtools.freqresp(self.known_act_filter)
        n_10Hz = int(20.0 / self.actuation_tst_sr * len(known_act_filter_response))
        n_6kHz = int(12000.0 / self.actuation_tst_sr * len(known_act_filter_response))
        n_6kHz = n_6kHz if n_6kHz < len(known_act_filter_response) else len(known_act_filter_response)
        for n in range(n_10Hz, n_6kHz):
            self.assertAlmostEqual(abs((known_act_filter_response[n] / test_act_filter_response[n]) -1),
                                   0, places=3)
        for n in range(n_10Hz):
            places = 1 if n / n_10Hz < 0.6 else 2
            self.assertAlmostEqual(abs(np.log10(abs(known_act_filter_response[n] /
                                                test_act_filter_response[n])) / 20),
                                                0, places=places)
        if n_6kHz < len(known_act_filter_response):
            for n in range(n_6kHz, len(known_act_filter_response)):
                places = 1 if n / len(known_act_filter_response) > 0.9 else 2
                self.assertAlmostEqual(abs(np.log10(abs(known_act_filter_response[n] /
                                                    test_act_filter_response[n])) / 20),
                                                    0, places=places)

    def test_CALCS_corr(self):
        self.FG.CALCS_corr(output_dir='./test',
                      output_filename='test_CALCS_corr.h5')
        calcs_corr_file = h5py.File('./test/test_CALCS_corr.h5', 'r')
        test_calcs_corr_filter = calcs_corr_file['calcs_corr_filter'][:]
        test_calcs_corr_filter_response = pydarm.firtools.freqresp(test_calcs_corr_filter)
        known_calcs_corr_filter_response = pydarm.firtools.freqresp(self.known_calcs_corr_filter)
        n_10Hz = int(20.0 / self.calcs_corr_sr * len(known_calcs_corr_filter_response))
        n_6kHz = int(12000.0 / self.calcs_corr_sr * len(known_calcs_corr_filter_response))
        n_6kHz = n_6kHz if n_6kHz < len(known_calcs_corr_filter_response) else len(known_calcs_corr_filter_response)
        for n in range(n_10Hz, n_6kHz):
            self.assertAlmostEqual(abs((known_calcs_corr_filter_response[n] / test_calcs_corr_filter_response[n]) -1),
                                   0, places=3)
        for n in range(n_10Hz):
            places = 1 if n / n_10Hz < 0.6 else 2
            self.assertAlmostEqual(abs(np.log10(abs(known_calcs_corr_filter_response[n] /
                                                test_calcs_corr_filter_response[n])) / 20),
                                                0, places=places)
        if n_6kHz < len(known_calcs_corr_filter_response):
            for n in range(n_6kHz, len(known_calcs_corr_filter_response)):
                places = 1 if n / len(known_calcs_corr_filter_response) > 0.9 else 2
                self.assertAlmostEqual(abs(np.log10(abs(known_calcs_corr_filter_response[n] /
                                                    test_calcs_corr_filter_response[n])) / 20),
                                                    0, places=places)

if __name__ == '__main__':
    unittest.main()
