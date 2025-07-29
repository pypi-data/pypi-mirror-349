===============
Time dependence
===============

The DARM loop parameters have time dependence that must be monitored and compensated in order to mitigate systematic errors. An approximated time-independent model of the sensing and actuation functions is installed in the "front end" computer system to computes a rough calibration. A complementary model that accounts for time-dependent variations of DARM loop parameters is also installed in the front end computer system. Calculation of the time dependent correction factors (TDCFs) is carried out via calibration lines measured with respect to reference model parameters installed as EPICS records.

Once a reference model has been finalized, the EPICS records are easily computed and can be written to the EPICS records system

>>> epics = darm.compute_epics_records(
... f_pcal1=17.1, f_uim=15.6, f_pum=16.4, f_tst=17.6,
... f_pcal2=410.3, f_pcal3=1083.7, arm='x')

Note that the ``compute_epics_records()`` method will be moved to the ``calcs`` module soon.
