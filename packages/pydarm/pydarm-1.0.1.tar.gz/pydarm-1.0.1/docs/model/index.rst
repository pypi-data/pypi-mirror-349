=====================
Making a pyDARM model
=====================

This page describes how pyDARM takes parameters supplied to construct
a model of the DARM servo loop. These parameters are used to compute
transfer functions between elements of the loop.

---------------
Quick reference
---------------

An example model file can be found `in the pyDARM git repository
<https://git.ligo.org/Calibration/pydarm/-/blob/master/example_model_files/H1_20190416.ini>`_.

-------
Details
-------

PyDARM models the DARM loop by drawing on parameters defined in a
configuration file or a configuration string. The configuration takes
the form of sections and key-value pairs. As an explicit example of
what a section and key-value pair looks like::

  [section]
  key = value

PyDARM sections mirror the parts of the interferometer we are
attempting to model::

  [sensing]
  [digital]
  [actuation]
  [actuation_x_arm]
  [actuation_y_arm]
  [pcal]
  [calcs]
  [FIR]

Other sections can also be defined::

  [metadata]
  [interferometer]

When modeling or estimating the uncertainty, more sections can be
included in the same configuration file or string or in a separate
file/string::

  [sensing-measurement]
  [x-arm-measurement]
  [y-arm-measurement]
  [x-arm-sus-cal-lines]
  [y-arm-sus-cal-lines]
  [x-arm-pcal-cal-lines]
  [y-arm-pcal-cal-lines]
  [tdcf-data]
  [sensing-tdcf]
  [x-arm-tdcf]
  [y-arm-tdcf]
  [hoft-tdcf-data-application]
  [sample-tdcf]
  [pcal]
  [epics-records-channels]

Within each section, key-value pairs need to be defined in order to
set parameters and compute transfer functions

>>> import pydarm
>>> import numpy
>>> frequencies = numpy.logspace(1, 3, 10)
>>> D = pydarm.darm.DigitalModel('''[digital]
... digital_filter_file = test/H1OMC_1239468752.txt
... digital_filter_bank = LSC_DARM1, LSC_DARM2
... digital_filter_modules = 1,2,3,4,7,9,10: 3,4,5,6,7
... digital_filter_gain = 400,1''')
>>> D.compute_response(frequencies)
array([5.98805825e+08-2.01229609e+09j,
       3.07291968e+09-6.39863354e+07j,
       4.46221271e+09+2.83011189e+09j,
       6.20899890e+09+6.53258031e+09j,
       1.02379652e+10+1.13041901e+10j,
       2.06788315e+10+1.56633213e+10j,
       4.46173195e+10+7.26147430e+09j,
       3.96197850e+10-7.25240470e+10j,
       1.16786264e+10-9.56665096e+10j,
       1.64517886e+06+1.22091523e+05j])

In the above example, we have have to point the pyDARM code at a
particular FOTON filter file in the ``test`` directory, so we set
``digital_filter_file = test/H1OMC_1239468752.txt``. We specify which
filter bank in the file that we are considering, separated by commas,
so we set ``digital_filter_bank = LSC_DARM1, LSC_DARM2``. In each
bank, the modules that we consider are comma-separated and the bank
lists are separated by a colon. So we set ``digital_filter_modules =
1,2,3,4,7,9,10: 3,4,5,6,7``. Lastly the gain of each bank is a
comma-separated list, so we set ``digital_filter_gain = 400,1``.

The full DARM loop can be specified via such sections and key-value
pairs. An example model file is shown `here
<https://git.ligo.org/Calibration/pydarm/-/blob/master/example_model_files/H1_20190416.ini>`_
and we use it to define an instance of a DARM model class (object) as:

>>> darm = pydarm.darm.DARMModel('H1_20190416.ini')

----------
Data files
----------

Certain files are needed in order to compute transfer functions of
DARM loop elements::

  [sensing]
  analog_anti_aliasing_file
  omc_filter_file

  [digital]
  digital_filter_file

  [actuation_x_arm]
  sus_filter_file
  suspension_file
  analog_anti_imaging_file

And any other transfer functions of associated calibration products::

  [pcal]
  pcal_filter_file
  analog_anti_aliasing_file

  [calcs]
  foton_invsensing_tf
  foton_delay_filter_tf
  foton_deltal_whitening_tf

Uncertainty estimation often requires data files of MCMC or GPR
posteriors HDF5 files.

These files are not provided as part of the pyDARM package, instead
being kept in a separate repository. PyDARM will attempt to open files
listed as values for the above keys prefixed by the following
preferred ordering:

#. The ``CAL_DATA_ROOT`` environment variable
#. The ``cal_data_root`` configuration key value

that is, ``CAL_DATA_ROOT`` environment variable overrides the
``cal_data_root`` configuration key value. For example, if data files are stored at
``/home/albert.einstein/Calibration/data_files/`` then setting
``CAL_DATA_ROOT=/home/albert.einstein/Calibration/data_files`` will
enable pyDARM to locate and open the files. If data files are stored
across many different directories, then ``CAL_DATA_ROOT`` can be set
to the path depth that is common amongst all the data files.

.. note:: Since different people may download DARM model configuration
	  files and store them in different locations, as well as any
	  repositories containing the necessary data files, it is
	  important to minimize hard-coding path names in
	  configuration files to as great a degree as is
	  possible. This minimizes the challeges and allows greater
	  use of DARM modeling.
