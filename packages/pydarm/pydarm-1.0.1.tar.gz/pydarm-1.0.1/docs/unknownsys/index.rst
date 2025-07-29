===================
Unknown systematics
===================

In the previous section, we saw how to take measurement data and
derive a best-fit set of parameters to the data. Those best-fit
parameters can be saved to a "library file" (i.e., a ``json`` file)
that keeps track of the measurement, model, fitting parameters, and
results.

>>> chain = meas.run_mcmc(fmin=30, fmax=5000, burn_in_steps=100, steps=100, save_to_file='example_sensing.json')

If we pass this ``json`` file as we initialize the process measurement
object, then we do not need to run another MCMC fit since the library
file already knows the results of that run. For example

>>> meas = pydarm.measurement.ProcessSensingMeasurement(
... 'H1_20210417.ini', meas1, meas2,
... ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC'),
... ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ'),
... meas1_cohThresh=0.9, meas2_cohThresh=0.9,
... json_results_file='example_sensing.json')

Multiple measurements can be stacked together and a Gaussian Progress
Regression calculation can be made via

>>> gpr = meas.run_gpr(frequencies, [meas], 30, 5000, [30], [5000])

--------
Plotting
--------

