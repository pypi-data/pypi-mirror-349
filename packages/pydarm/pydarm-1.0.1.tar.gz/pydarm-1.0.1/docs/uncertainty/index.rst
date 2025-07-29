==================
Uncertainty budget
==================

An uncertainty budget can be estimated with the following inputs:

#. reference model parameter configuration string/file
#. MCMC measurements of model parameters (sensing and actuation) saved
   in HDF5 files
#. Time-dependent correction factors (TDCFs) as measured by the
   calibration lines (queried via NDS2)
#. Residual unknown systematic error measured by stacked measurements
   and saved in HDF5 files
#. systematic error of the photon calibrator

An example configuration file for the uncertainty budget can be found
at `in the pyDARM git repository
<https://git.ligo.org/Calibration/pydarm/-/blob/master/example_model_files/H1_20190416_uncertainty.ini>`_.

First we initialize a ``DARMUncertainty`` object and then we can draw
random samples from the object:

>>> test_unc = pydarm.uncertainty.DARMUncertainty(
... 'H1_20190416.ini', uncertainty_config='H1_20190416_uncertainty.ini')
>>> samples = test_unc.compute_response_uncertainty(
... 1239958818, frequencies, trials=10)

.. note:: The uncertainty budget configuration file can be combined with
	  the original DARM model configuration file into a single
	  file. For convenience if there is anything provided in the
	  ``uncertainty_config`` argument, it will override any
	  key-value in the model configuration.

--------
Plotting
--------

