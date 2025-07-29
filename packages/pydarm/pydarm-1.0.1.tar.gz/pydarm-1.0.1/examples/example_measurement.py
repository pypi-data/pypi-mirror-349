import numpy as np
from pydarm import measurement
from matplotlib import pyplot as plt


"""
Example code on how to use the following methods from measurement.py:
    - get_raw_tf
    - get_set_of_channels
    - get_raw_asd
"""
# EXAMPLE 1: Dealing with a SweptSine measurement file.

# These are the xml files we want to get our data from.
measurement_file_1 = \
    '../test/2020-01-03_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml'

meas_obj_1 = measurement.Measurement(measurement_file_1)
channelA_1 = 'H1:LSC-DARM1_IN2'
channelB_1 = 'H1:LSC-DARM1_IN1'

temp_freq, temp_tf, temp_coh, temp_unc = meas_obj_1.get_raw_tf(channelA_1,
                                                               channelB_1,
                                                               cohThresh=0.0)

plt.figure(1)
plt.subplot(211)
plt.loglog(temp_freq,
           np.abs(temp_tf), 'ro')

plt.subplot(212)
plt.semilogx(temp_freq,
             np.angle(temp_tf, deg=True), 'ro')
# plt.savefig('../../../public_html/plot_result_1.pdf', format='pdf')
plt.show(block=True)

# Examples of other information you can get from the measurement class:
print('----------------------------------------------------')
print('Other information in file ', measurement_file_1)
print('GPS of measurement is ', meas_obj_1.gps_time)
print('Navg of measurement is ', meas_obj_1.averages)
print('Bandwidth of measurement is ', meas_obj_1.bw)

set_of_A_channels_1, set_of_B_channels_1 = meas_obj_1.get_set_of_channels()
print('A Channels in measurement file are:', set_of_A_channels_1)
print('B (NON A) Channels in measurement file are:', set_of_B_channels_1)
print('----------------------------------------------------')

# ----------------------------------------------------------------
# ----------------------------------------------------------------

# EXAMPLE 2: Dealing with an FFT dtt file.

# The following lines show an example of ASD extraction from a dtt
# file that contains FFT (or BroadBand data)

# These are the xml files we want to get our data from.
measurement_file_2 = \
    '../test/2019-03-27_H1DARM_OLGTF_BB.xml'

meas_obj_2 = measurement.Measurement(measurement_file_2)
channelA_2 = 'H1:LSC-DARM1_IN2'
channelB_2 = 'H1:LSC-DARM1_IN1'
channelA_freq, channelA_asd = meas_obj_2.get_raw_asd(channelA_2)
channelB_freq, channelB_asd = meas_obj_2.get_raw_asd(channelB_2)

# print(channelA_asd)

plt.figure(2)
plt.loglog(channelA_freq, channelA_asd, 'k',
           channelB_freq, channelB_asd, 'r')
plt.show(block=True)
# Examples of other information you can get from the measurement class:
print('----------------------------------------------------')
print('Other information in measurement file: ', measurement_file_2)
print('GPS of measurement is ', meas_obj_2.gps_time)
print('Navg of measurement is ', meas_obj_2.averages)
print('Bandwidth of measurement is ', meas_obj_2.bw)

set_of_A_channels_2, set_of_B_channels_2 = meas_obj_2.get_set_of_channels()
print('A Channels in measurement file are:', set_of_A_channels_2)
print('B (NON A) Channels in measurement file are:', set_of_B_channels_2)
print('----------------------------------------------------')
# ----------------------------------------------------------------------
