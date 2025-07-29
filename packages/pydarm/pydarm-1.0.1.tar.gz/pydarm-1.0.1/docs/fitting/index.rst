=================
Fitting data
=================

This section covers how ``pyDARM`` takes in a model configuration
string/file, measurement files, and can compute best-fit parameters
to the measured data. This section assumes that transfer functions
(swept sine or broadband) have been computed and saved in ``diaggui``
XML files.

--------------------------------
Sensing function fitting example
--------------------------------

First, initialize the measurement objects:

>>> meas1 = pydarm.measurement.Measurement(
... '2021-04-17_H1_DARM_OLGTF_LF_SS_5to1100Hz_15min.xml')
>>> meas2 = pydarm.measurement.Measurement(
... 2021-04-17_H1_PCAL2DARMTF_LF_SS_5t1100Hz_10min.xml')

Next, define the process measurement type and parameters for the data
processing:

>>> meas = pydarm.measurement.ProcessSensingMeasurement(
... 'H1_20210417.ini', meas1, meas2,
... ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
... ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
... meas1_cohThresh=0.9, meas2_cohThresh=0.9)

Finally, we can call the ``run_mcmc()`` method to run the actual
fit. Here, we have some additional controls over the fitting
parameters

>>> chain = meas.run_mcmc(fmin=30, fmax=5000, burn_in_steps=100, steps=100)
>>> np.median(chain, axis=0)
[3.43929865e+06 4.50565641e+02 4.30953443e+00 30.95380056e+00 6.57319811e-06]

A corner plot can be made from the posterior chain

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Processed data versus best-fit model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First get the data from the ``meas`` object

>>> freq, tf, unc = meas.get_processed_measurement_response()

Next compute the best-fit model response

>>> from scipy.signal import freqresp
>>> MAP = np.median(chain, axis=0)
>>> model_response = (MAP[0] *
... freqresp(darm.sensing.SensingModel.optical_response(
... MAP[1], MAP[2], MAP[3], darm.sensing.is_pro_spring)
... 2*np.pi*frequencies)[1] *
... np.exp(-2*np.pi*1j*MAP[4]*frequencies))

--------
Plotting
--------

A comparison plot can be made via

>>> pydarm.plot.residuals(frequencies, model_response, freq, tf, unc, show=True)

