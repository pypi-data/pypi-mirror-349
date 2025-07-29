import unittest
import pydarm
import numpy as np
import os
import tempfile


class TestHwinjPcalActuation(unittest.TestCase):

    def setUp(self):
        # Pre-computed values
        self.frequencies = np.logspace(0, np.log10(5000.), 10)
        self.model_string = '''
[sensing]
x_arm_length = 3994.4704
y_arm_length = 3994.4692
[actuation]
[actuation_x_arm]
suspension_file = test/H1susdata_O3.mat
[pcal]
pcal_incidence_angle        = 8.8851
pcalx_etm_watts_per_ofs_volt = 0.13535
dac_gain = 7.62939453125e-05
analog_anti_aliasing_file = test/H1aa.mat
anti_aliasing_rate_string = 16k
anti_aliasing_method = biquad
'''
        self.known_calib = np.array(
            [-7.054261809347476e-21-2.5792073975006035e-20j,
             -1.7642763701489958e-21+5.529873095262561e-24j,
             -2.4952736339480573e-22+2.685090040213818e-24j,
             -3.727031662976503e-23+1.053258748290209e-24j,
             -5.595731229858602e-24+4.09166391929794e-25j,
             -8.303561387390279e-25+1.5808704794395063e-25j,
             -1.1276579464353648e-25+5.940127944020822e-26j,
             -6.069632982961961e-27+1.8329055930136462e-26j,
             2.9790307450926445e-27-3.429464113259114e-28j,
             3.6001529764192544e-28+2.3945209956343304e-28j])

    def tearDown(self):
        del self.frequencies
        del self.model_string
        del self.known_calib

    def test_hwinj_pcal_actuation(self):
        """ Test the hardware injection actuation function"""
        hwinj = pydarm.hwinj.HwinjModel(self.model_string)
        tf = hwinj.hwinj_pcal_actuation(self.frequencies)
        for n in range(len(self.frequencies)):
            self.assertAlmostEqual(
                np.abs(tf[n] / self.known_calib[n]), 1)
            self.assertAlmostEqual(
                np.angle(tf[n] / self.known_calib[n], deg=True), 0)

    def test_save_hwinj_pcal_actuation(self):
        hwinj = pydarm.hwinj.HwinjModel(self.model_string)
        with tempfile.TemporaryDirectory() as d:
            save_file = os.path.join(d, 'test_hwinj_out')
            hwinj.save_hwinj_pcal_actuation(self.frequencies, save_file)
            data = np.loadtxt(save_file, comments='%')
            for n in range(len(data)):
                self.assertAlmostEqual(data[n, 0] / self.frequencies[n], 1)
                self.assertAlmostEqual(
                    data[n, 1] / np.abs(self.known_calib[n]), 1)
                self.assertAlmostEqual(
                    data[n, 2], np.angle(self.known_calib[n]))


if __name__ == '__main__':
    unittest.main()
