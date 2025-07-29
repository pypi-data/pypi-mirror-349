import pytest
uncertainty = pytest.importorskip("pydarm.uncertainty")

import unittest
import numpy as np
from gwpy.timeseries import TimeSeriesDict as tsd
import os
import pandas as pd

from pydarm import utils
from pydarm.darm import DARMModel


class TestTdcfMeanValues(unittest.TestCase):

    def setUp(self):
        self.known_values = np.array(
            [404.9034118652344,
             1.001456618309021,
             1.000232577323914,
             1.001761555671692,
             0.9874549508094788,
             0.001804656465537846,
             0.001688393531367183,
             0.001474045449867845,
             0.001592247281223536,
             0.001256731105968356])

    def tearDown(self):
        del self.known_values

    def test_tdcf_mean_values(self):
        data = tsd.read('./test/test_ch_data.hdf5')
        for idx, name in enumerate(list(data)):
            mean = np.mean(data[name].value)
            self.assertAlmostEqual(mean, self.known_values[idx])


class TestSampleLineUncertainty(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')

    def tearDown(self):
        del self.data

    def test_no_uncertainty(self):
        config = '''[sensing-tdcf]
pcal2_unc = 0
[x-arm-tdcf]
pcal1_unc = 0
uim_unc = 0
pum_unc = 0
tst_unc = 0
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False'''
        ini = './example_model_files/H1_20190416.ini'

        test_unc = uncertainty.DARMUncertainty(ini, config)
        a, b, c = test_unc.sample_line_uncertainty(1239958818, data=self.data)
        self.assertAlmostEqual(a, 1)
        for n in range(len(b)):
            self.assertAlmostEqual(b[n], 1)
            self.assertAlmostEqual(c[n], 1)

    def test_sample_line_uncertainty(self):
        config = '''[sensing-tdcf]
[x-arm-tdcf]
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False'''

        ini = './example_model_files/H1_20190416.ini'
        test_unc = uncertainty.DARMUncertainty(ini, config)
        a, b, c = test_unc.sample_line_uncertainty(1239958818, data=self.data)
        self.assertAlmostEqual(a, 1, places=2)
        for n in range(len(b)):
            self.assertAlmostEqual(b[n], 1, places=2)
            self.assertAlmostEqual(c[n], 1, places=2)


class TestSamplePcalUnc(unittest.TestCase):

    def setUp(self):
        self.expected = 1

    def tearDown(self):
        del self.expected

    def test_sample_pcal_unc(self):
        test = uncertainty.DARMUncertainty.sample_pcal_unc(err=1, unc=0)

        self.assertAlmostEqual(test, self.expected)


class TestGetModelPars(unittest.TestCase):

    def setUp(self):
        self.config = '''
[sensing]
coupled_cavity_optical_gain   = 3.22e6
coupled_cavity_pole_frequency = 410.6
detuned_spring_frequency      = 4.468
detuned_spring_Q              = 52.14
single_pole_approximation_delay_correction = -12e-6
[digital]
[actuation]
[actuation_x_arm]
uim_NpA       = 1.634
pum_NpA       = 0.02947
tst_NpV2      = 4.427e-11
uim_delay = 0
pum_delay = 0
tst_delay = 0
'''

    def tearDown(self):
        del self.config

    def test_get_model_pars(self):
        darm = DARMModel(self.config)

        sens_pars, act_pars = uncertainty.DARMUncertainty.get_model_pars(darm)
        self.assertAlmostEqual(sens_pars['gain'],
                               darm.sensing.coupled_cavity_optical_gain)
        self.assertAlmostEqual(sens_pars['f_cc'],
                               darm.sensing.coupled_cavity_pole_frequency)
        self.assertAlmostEqual(sens_pars['f_s'],
                               darm.sensing.detuned_spring_frequency)
        self.assertAlmostEqual(sens_pars['Q'],
                               darm.sensing.detuned_spring_q)
        self.assertAlmostEqual(sens_pars['single_pole_delay_corr'],
                               darm.sensing.single_pole_approximation_delay_correction)
        self.assertAlmostEqual(act_pars['xarm']['UIM'][0],
                               darm.actuation.xarm.uim_npa)
        self.assertAlmostEqual(act_pars['xarm']['PUM'][0],
                               darm.actuation.xarm.pum_npa)
        self.assertAlmostEqual(act_pars['xarm']['TST'][0],
                               darm.actuation.xarm.tst_npv2)
        self.assertAlmostEqual(act_pars['xarm']['UIM'][1],
                               darm.actuation.xarm.uim_delay)
        self.assertAlmostEqual(act_pars['xarm']['PUM'][1],
                               darm.actuation.xarm.pum_delay)
        self.assertAlmostEqual(act_pars['xarm']['TST'][1],
                               darm.actuation.xarm.tst_delay)


class TestSampleResponse(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        
        os.environ['CAL_DATA_ROOT'] = './test'
        """
        The reference data was generated by the following:
        ref_model = pydarm.darm.DARMModel('./example_model_files/H1_20190416.ini')
        ref_model.sensing.coupled_cavity_optical_gain *= 1.001456618309021
        ref_model.sensing.coupled_cavity_pole_frequency = 404.9034118652344
        ref_model.actuation.xarm.uim_npa *= 0.9874549508094788
        ref_model.actuation.xarm.pum_npa *= 1.0002325773239136
        ref_model.actuation.xarm.tst_npv2 *= 1.001761555671692
        known_response = ref_model.compute_response_function(self.frequencies)
        """
        self.known_response = np.array(
            [2.028504986095783-0.3875242485008085j,
             0.001141684700656659-0.004462191049044788j,
             7.183993452924785e-06-1.428672439631115e-06j,
             -6.508352356473097e-07+1.554166057335518e-07j,
             -2.19294725075012e-09-1.989291669099206e-07j,
             1.672640015694479e-07+2.137038974884646e-08j,
             2.112268336596777e-07+3.617519908798565e-07j,
             -7.522130216217252e-08+6.428161477749937e-07j,
             -1.482755716524026e-06+3.028370715328025e-07j,
             4.522732922137328e-06-1.53996316224857e-06j])

    def tearDown(self):
        del self.data
        del self.frequencies
        del self.known_response
        del os.environ['CAL_DATA_ROOT']

    def test_sample_response_no_tdcf_application(self):
        config = '''[sensing-measurement]
mcmc =
gpr =
[x-arm-measurement]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[pcal]
sys_err =
sys_unc =
sample = False'''

        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', config)
        test_response, data, c_pars, a_pars, c_syserr, a_syserr = \
            test_unc.sample_response(
                1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[0][n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[0][n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)

    def test_sample_response(self):
        config2 = '''[sensing-measurement]
mcmc =
gpr =
[x-arm-measurement]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = 0
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = 0
uim_unc = 0
pum_unc = 0
tst_unc = 0
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = True
kappa_pum = True
kappa_tst = True
[pcal]
sys_err = 1
sys_unc = 0
sample = True'''

        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', config2)
        test_response, data, c_pars, a_pars, c_syserr, a_syserr = \
            test_unc.sample_response(
                1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[0][n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[0][n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)


class TestNominalResponse(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.config = '''[sensing-measurement]
mcmc =
gpr =
[x-arm-measurement]
tst_mcmc =
pum_mcmc =
uim_mcmc =
tst_gpr =
pum_gpr =
uim_gpr =
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = True
[pcal]
sys_err = 1'''

        """
        The reference data was generated by the following:
        ref_model = pydarm.darm.DARMModel('./example_model_files/H1_20190416.ini')
        ref_model.sensing.coupled_cavity_optical_gain = 3224690.3109550476
        ref_model.sensing.coupled_cavity_pole_frequency = 404.9034118652344
        ref_model.actuation.xarm.uim_npa = 1.6135013896226882
        ref_model.actuation.xarm.pum_npa = 0.029476854053735745
        ref_model.actuation.xarm.tst_npv2 = 4.43479840695858e-11
        known_response = ref_model.compute_response_function(self.frequencies)
        """
        self.known_response = np.array(
            [2.028504986095783-0.3875242485008085j,
             0.001141684700656659-0.004462191049044788j,
             7.183993452924785e-06-1.428672439631115e-06j,
             -6.508352356473097e-07+1.554166057335518e-07j,
             -2.19294725075012e-09-1.989291669099206e-07j,
             1.672640015694479e-07+2.137038974884646e-08j,
             2.112268336596777e-07+3.617519908798565e-07j,
             -7.522130216217252e-08+6.428161477749937e-07j,
             -1.482755716524026e-06+3.028370715328025e-07j,
             4.522732922137328e-06-1.53996316224857e-06j])
        os.environ['CAL_DATA_ROOT'] = './test'

        # Known response with sensing, PUM actuation stage using TST delay
        # Assume sensing MCMC had 2 usec delay and TST delay had 3 usec advance
        self.known_response_with_mcmc_delay = np.array(
            [2.0284918672188783-0.38750451482907217j,
             0.001141879404450972-0.004462049611582206j,
             7.18427264681572e-06-1.4274693756364452e-06j,
             -6.511010632231071e-07+1.552522730588147e-07j,
             -2.391860029684992e-09-1.9888580485829746e-07j,
             1.6703628173386567e-07+2.1881047943440604e-08j,
             2.1015930754874738e-07+3.626627175452703e-07j,
             -8.137500634451934e-08+6.421292314668346e-07j,
             -1.4896997420727998e-06+2.6658857029827334e-07j,
             4.610503437335776e-06-1.2529396436830116e-06j])

    def tearDown(self):
        del self.data
        del self.frequencies
        del self.config
        del self.known_response
        del self.known_response_with_mcmc_delay
        del os.environ['CAL_DATA_ROOT']

    def test_nominal_response(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)
        
        test_response, data = test_unc.nominal_response(
            1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_response[n]) / np.abs(self.known_response[n]), 1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response[n], deg=True), 0.0, places=5)

    def test_nominal_response_with_mcmc_delays(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)

        # generate the "random" samples to get the median for time delay
        # (no correlation)
        sensing_posteriors = np.random.normal(
            loc=[0, 0, 0, 0, 2e-6],
            scale=[0, 0, 0, 0, 0],
            size=(1, 5))
        tst_posteriors = np.random.normal(
            loc=[0, -3e-6], scale=[0]*2, size=(1,2))

        test_unc.sensing_mcmc_chain = [None]*5
        test_unc.sensing_mcmc_chain[4] = sensing_posteriors
        test_unc.actuation_mcmc_dict['xarm'].update({'PUM': [None]*5})
        test_unc.actuation_mcmc_dict['xarm'].update({'TST': [None]*5})
        test_unc.actuation_mcmc_dict['xarm']['PUM'][4] = tst_posteriors
        test_unc.actuation_mcmc_dict['xarm']['TST'][4] = tst_posteriors
        test_unc.act_delay_sample_dict['xarm'].setdefault('PUM', 'TST')

        # compute nominal response
        test_response, data = test_unc.nominal_response(
            1239958818, self.frequencies, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(
                    test_response[n]/self.known_response_with_mcmc_delay[n]),
                1.0)
            self.assertAlmostEqual(
                np.angle(test_response[n], deg=True) -
                np.angle(self.known_response_with_mcmc_delay[n], deg=True),
                0.0, places=5)


class TestComputeResponseUncertainty(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.config = '''[sensing-measurement]
mcmc = 
gpr = 
[x-arm-measurement]
tst_mcmc = 
pum_mcmc = 
uim_mcmc = 
tst_gpr = 
pum_gpr = 
uim_gpr = 
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = False
[pcal]
sys_err =
sys_unc =
sample = False'''

        self.known_ratio = np.ones(len(self.frequencies), dtype='complex128')
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.data
        del self.frequencies
        del os.environ['CAL_DATA_ROOT']
        del self.known_ratio
        del self.config

    def test_compute_response_uncertainty(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)
        
        samples = test_unc.compute_response_uncertainty(
            1239958818, self.frequencies, trials=50, data=self.data)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(samples[0][n]) / np.abs(self.known_ratio[n]), 1.0,
                places=6)
            self.assertAlmostEqual(
                np.angle(samples[0][n], deg=True) -
                np.angle(self.known_ratio[n], deg=True), 0.0, places=5)

    def test_compute_response_uncertainty_shift(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)
        
        samples = test_unc.compute_response_uncertainty(
            1239958818, self.frequencies, trials=1, data=self.data,
            shift_sample_tf=1.1*np.ones(len(self.frequencies), dtype='complex128'))

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(samples[0][n]) / np.abs(self.known_ratio[n]), 1.1,
                places=6)
            self.assertAlmostEqual(
                np.angle(samples[0][n], deg=True) -
                np.angle(self.known_ratio[n], deg=True), 0.0, places=5)


class TestComputeResponseUncertaintyWithMonitorLines(unittest.TestCase):

    def setUp(self):
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.config = '''[sensing-measurement]
mcmc = 
gpr = 
[x-arm-measurement]
tst_mcmc = 
pum_mcmc = 
uim_mcmc = 
tst_gpr = 
pum_gpr = 
uim_gpr = 
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = False
[pcal]
sys_err =
sys_unc =
sample = False'''

        self.response_unc_mag = np.abs(np.ones((3, len(self.frequencies)), dtype='complex128'))
        self.response_unc_phase = np.angle(np.ones((3, len(self.frequencies)), dtype='complex128'))
        # H1 data collected the 130 sec surrounding
        # 22 May 2023 00:00 UTC [1368820753, 1368820883)
        # Manually copied into this data format
        self.monitor_line_data = pd.DataFrame.from_dict(
            {'oscillator_frequency': [17.10, 17.10, 33.43, 33.43, 53.67, 53.67, 77.73, 77.73, 102.13, 102.13, 283.91, 283.91, 284.01, 284.01, 410.30, 410.30, 1083.70, 1083.70],
             'TF_mag': [1.067940, 1.070224, 1.045985, 1.040859, 0.975387, 0.978917, 0.937758, 0.938154, 0.952788, 0.948777, 1.013140, 1.014714, 1.011554, 1.011681, 1.000881, 1.000905, 1.001902, 1.007867],
             'TF_phase': [2.327334, 2.176462, -2.945425, -3.002312, -3.889601, -3.526476, 0.136221, 0.143934, 0.985192, 1.327699, -0.097977, -0.096689, -0.205736, -0.179942, 0.083392, 0.017111, -0.043278, -0.435806]})
        self.known_ratio_mag = np.array(
                [[0.99972891, 0.99990845, 0.99964301, 0.98114327, 0.97248649,
                  0.97131506, 0.99653361, 0.99803425, 0.99961665, 0.99987037],
                 [1.00000168, 1.00000021, 1.00000447, 1.005188,   0.99814108,
                  0.9971826,  1.00220231, 1.00099026, 1.00000776, 1.00000062],
                 [1.00027444, 1.00009197, 1.00036593, 1.02923272, 1.02379568,
                  1.02305014, 1.00787102, 1.00394626, 1.00039888, 1.00013087]])
        self.known_ratio_phase = np.array(
                [[-5.05386967e-04, -1.22655696e-04, -3.16380004e-04, -1.15518643e-02,
                  -3.57576523e-02, -7.17064516e-03, -1.87701400e-03, -2.59521180e-03,
                  -6.09973589e-04, -1.85258024e-04],
                 [3.56156229e-06, 9.13787446e-07, 2.64386731e-06, 2.53481728e-03,
                  2.83286151e-03, 1.51861046e-04, -4.97705204e-04, -3.39435997e-04,
                  -3.40283254e-05, -1.08261589e-07],
                 [5.12510092e-04, 1.24483271e-04, 3.21667739e-04, 1.66214989e-02,
                  4.14233753e-02, 7.47436726e-03, 8.81603591e-04, 1.91633981e-03,
                  5.41916938e-04, 1.85041501e-04]])
        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.frequencies
        del os.environ['CAL_DATA_ROOT']
        del self.response_unc_mag
        del self.response_unc_phase
        del self.monitor_line_data
        del self.known_ratio_mag
        del self.known_ratio_phase 
        del self.config

    def test_compute_response_uncertainty_with_monitor_lines(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)

        response_mag_quant, response_pha_quant = test_unc.response_uncertainty_combine_with_mon_line_data(
            self.frequencies, self.response_unc_mag, self.response_unc_phase,
            self.monitor_line_data, seed=1234)

        for m in range(3):
            for n in range(len(self.response_unc_mag[0, :])):
                self.assertAlmostEqual(response_mag_quant[m, n] / self.known_ratio_mag[m, n], 1.0, places=6)
                self.assertAlmostEqual(np.angle(response_pha_quant[m, n], deg=True) - np.angle(self.known_ratio_phase[m, n], deg=True), 0.0, places=5)


class TestComputeConvolvedResponseUncertainty(unittest.TestCase):

    def setUp(self):
        self.data = tsd.read('./test/test_ch_data.hdf5')
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.config = '''[reference-model]
model =
previous_model_response_curve_file = test/test_response_curves.hdf5
[sensing-measurement]
mcmc = 
gpr = 
[x-arm-measurement]
tst_mcmc = 
pum_mcmc = 
uim_mcmc = 
tst_gpr = 
pum_gpr = 
uim_gpr = 
[tdcf-data]
frametype = R
duration = 130
line_unc_th = 0.005
[sensing-tdcf]
kappa_c = CAL-CS_TDEP_KAPPA_C_OUTPUT
f_cc = CAL-CS_TDEP_F_C_OUTPUT
pcal2_unc = CAL-CS_TDEP_PCAL_LINE2_UNCERTAINTY
pcal_arm = Y
[x-arm-tdcf]
kappa_uim = CAL-CS_TDEP_KAPPA_UIM_REAL_OUTPUT
kappa_pum = CAL-CS_TDEP_KAPPA_PUM_REAL_OUTPUT
kappa_tst = CAL-CS_TDEP_KAPPA_TST_REAL_OUTPUT
pcal1_unc = CAL-CS_TDEP_PCAL_LINE1_UNCERTAINTY
uim_unc = CAL-CS_TDEP_SUS_LINE1_UNCERTAINTY
pum_unc = CAL-CS_TDEP_SUS_LINE2_UNCERTAINTY
tst_unc = CAL-CS_TDEP_SUS_LINE3_UNCERTAINTY
pcal_arm = Y
[sample-tdcf]
kappa_c = False
f_cc = False
kappa_uim = False
kappa_pum = False
kappa_tst = False
[hoft-tdcf-data-application]
kappa_c = True
f_cc = True
kappa_uim = True
kappa_pum = True
kappa_tst = True
pcal_sys_err = False
[pcal]
sys_err =
sys_unc = 0.01
sample = True'''

        os.environ['CAL_DATA_ROOT'] = './test'

    def tearDown(self):
        del self.data
        del self.frequencies
        del os.environ['CAL_DATA_ROOT']
        del self.config
        

    def test_compute_response_uncertainty_convolution(self):
        test_unc = uncertainty.DARMUncertainty(
            'example_model_files/H1_20190416.ini', self.config)

        samples = test_unc.compute_response_uncertainty(
            1239958818, self.frequencies, trials=5, data=self.data,
            seed=1234)

        _, old_samples = utils.read_response_curves_from_hdf5(
            test_unc.response_curve_file)

        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(samples[0][n]) / np.abs(old_samples[0][n])**2, 1.0,
                places=6)
            self.assertAlmostEqual(
                np.angle(samples[0][n], deg=True) -
                2 * np.angle(old_samples[0][n], deg=True), 0.0, places=5)

class TestResponseQuantiles(unittest.TestCase):

    def setUp(self):
        self.response_samples = np.ones((10, 10), dtype='complex128')
        self.response_samples[0:4, :] *= 0.8
        self.response_samples[5:9, :] *= 1.2

    def tearDown(self):
        del self.response_samples

    def test_response_quantiles(self):
        response_mag_quant, response_pha_quant = \
          uncertainty.DARMUncertainty.response_quantiles(
              self.response_samples)

        for m in range(3):
            for n in range(len(self.response_samples[0, :])):
                self.assertAlmostEqual(response_mag_quant[m, n], [0.8, 1, 1.2][m])
                self.assertAlmostEqual(response_pha_quant[m, n], 0)


class TestPlotResponseSamples(unittest.TestCase):

    def setUp(self):
        self.response_samples = np.ones((10, 10), dtype='complex128')
        self.freq = np.logspace(0, np.log10(5000.), 10)
        self.response_mag_quant, self.response_pha_quant = \
          uncertainty.DARMUncertainty.response_quantiles(
              self.response_samples)
        self.ifo = 'LHO'

    def tearDown(self):
        del self.response_samples
        del self.freq
        del self.response_mag_quant
        del self.response_pha_quant
        del self.ifo

    def test_plot_response_samples(self):
        uncertainty.DARMUncertainty.plot_response_samples(
            self.freq, self.response_mag_quant, self.response_pha_quant, self.ifo)
