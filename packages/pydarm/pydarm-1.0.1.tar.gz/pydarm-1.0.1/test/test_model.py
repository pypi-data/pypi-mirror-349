import unittest
import pydarm
import numpy as np


class TestAnalogAAOrAIFilterResponse(unittest.TestCase):

    def setUp(self):
        self.config = '''
[sensing]
analog_anti_aliasing_file = test/H1aa.mat
'''
        self.config2 = '''
[sensing]
analog_anti_aliasing_file = test/H1aa.mat, test/H1aa.mat
'''
        self.config3 = '''
[actuation_x_arm]
analog_anti_imaging_file = test/H1aa.mat
'''
        self.config4 = '''
[sensing]
analog_anti_aliasing_file = 
'''
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [0.9902583151820756-0.00023625869326662408j,
             0.9902581352102275-0.0006086735508483027j,
             0.990256940678447-0.001568125690903292j,
             0.9902490122026717-0.00403995033942778j,
             0.9901963893790059-0.010407889389582571j,
             0.9898471618373895-0.02680975201205813j,
             0.9875313105265322-0.06899983685404412j,
             0.9722512045409587-0.17657342104176357j,
             0.8745742785659897-0.43547246366239517j,
             0.3390985734013402-0.8563173043598763j])
        self.known_response_2 = np.ones(len(self.frequencies),
                                        dtype='complex128')

    def tearDown(self):
        del self.config
        del self.config2
        del self.config3
        del self.config4
        del self.frequencies
        del self.known_response
        del self.known_response_2

    def test_analog_aa_or_ai_filter_response(self):
        test_aa = pydarm.sensing.SensingModel(self.config)
        test_aa_response = test_aa.analog_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))

    def test_analog_aa_or_ai_filter_response_2(self):
        test_aa = pydarm.sensing.SensingModel(self.config2)
        test_aa_response = test_aa.analog_aa_or_ai_filter_response(
            self.frequencies, idx=1)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))

    def test_analog_aa_or_ai_filter_response_3(self):
        test_ai = pydarm.actuation.ActuationModel(
            self.config3, measurement='actuation_x_arm')
        test_ai_response = test_ai.analog_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_ai_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(test_ai_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))

    def test_analog_aa_or_ai_filter_response_4(self):
        test_aa = pydarm.sensing.SensingModel(self.config4)
        test_aa_response = test_aa.analog_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response_2[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response_2[n], deg=True))


class TestDigitalAAOrAIFilterResponse(unittest.TestCase):

    def setUp(self):
        self.config = '''
[sensing]
anti_aliasing_rate_string = 16k
anti_aliasing_method      = biquad
'''
        self.config2 = '''
[sensing]
anti_aliasing_rate_string = 512k-daq, 16k
anti_aliasing_method      = biquad, biquad
'''
        self.config3 = '''
[actuation_x_arm]
anti_imaging_rate_string = 16k
anti_imaging_method      = biquad
'''
        self.config4 = '''
[sensing]
anti_aliasing_rate_string =
anti_aliasing_method      =
'''
        self.config5 = '''
[sensing]
anti_aliasing_rate_string = 524k
anti_aliasing_method      = biquad
'''
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.known_response = np.array(
            [1.0000006743118521-0.00026859554703262606j,
             1.0000005577918698-0.0006919831728579482j,
             0.9999997844069123-0.0017827587938075234j,
             0.9999946510415249-0.004592951080196375j,
             0.9999605723740017-0.011833290098468159j,
             0.9997340799606691-0.03049404992719877j,
             0.9982174966256611-0.07869700811767119j,
             0.9875624565339749-0.20500805282580065j,
             0.8902071582110597-0.5598509390584541j,
             -0.3367135303069774-1.013081908852281j])
        self.known_response_2 = np.array(
            [0.9999990382402011-0.0004319068840388653j,
             0.9999986023793369-0.0011127222912309769j,
             0.9999957094228397-0.0028667077636213827j,
             0.9999765077161654-0.007385499465433574j,
             0.9998490507274017-0.01902720882007928j,
             0.9990026826865991-0.04901872479597216j,
             0.9933677211236748-0.1262669994944426j,
             0.9552099549118505-0.3248211559942308j,
             0.6716089707864071-0.8118322341065793j,
             -0.9845070556065999-0.4321416428115297j])
        self.known_response_3 = np.ones(len(self.frequencies),
                                        dtype='complex128')
        self.known_response_4 = np.array(
            [0.9999959146066341-9.074813388897661e-05j,
             0.9999958914215733-0.00023379454162619835j,
             0.9999957375346976-0.0006023251762471174j,
             0.9999947161370252-0.0015517707525287735j,
             0.9999879367903267-0.003997821722137085j,
             0.9999429402799624-0.01029946679488665j,
             0.9996442943408302-0.0265323617183539j,
             0.9976625525293799-0.06831829827324934j,
             0.9845292613057995-0.17537755757711357j,
             0.8981087295015726-0.44131250317257753j])

    def tearDown(self):
        del self.config
        del self.config2
        del self.config3
        del self.config4
        del self.config5
        del self.frequencies
        del self.known_response
        del self.known_response_2
        del self.known_response_3
        del self.known_response_4

    def test_digital_aa_or_ai_filter_response(self):
        test_aa = pydarm.sensing.SensingModel(self.config)
        test_aa_response = test_aa.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))

    def test_digital_aa_or_ai_filter_response_2(self):
        test_aa = pydarm.sensing.SensingModel(self.config2)
        test_aa_response = test_aa.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response_2[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response_2[n], deg=True))

    def test_digital_aa_or_ai_filter_response_3(self):
        test_ai = pydarm.actuation.ActuationModel(
            self.config3, measurement='actuation_x_arm')
        test_ai_response = test_ai.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_ai_response[n]),
                np.abs(self.known_response[n]))
            self.assertAlmostEqual(
                np.angle(test_ai_response[n], deg=True),
                np.angle(self.known_response[n], deg=True))

    def test_digital_aa_or_ai_filter_response_4(self):
        test_aa = pydarm.sensing.SensingModel(self.config4)
        test_aa_response = test_aa.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response_3[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response_3[n], deg=True))

    def test_digital_aa_or_ai_filter_response_5(self):
        test_aa = pydarm.sensing.SensingModel(self.config5)
        test_aa_response = test_aa.digital_aa_or_ai_filter_response(
            self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(test_aa_response[n]),
                np.abs(self.known_response_4[n]))
            self.assertAlmostEqual(
                np.angle(test_aa_response[n], deg=True),
                np.angle(self.known_response_4[n], deg=True))
