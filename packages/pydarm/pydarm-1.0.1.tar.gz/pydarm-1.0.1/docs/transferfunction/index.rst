============================
Computing transfer functions
============================

We saw in the last section how a DARM model can be defined as a
configuration string or file. Here is an example of defining the model
in a configuration file

>>> darm = pydarm.darm.DARMModel('H1_20190416.ini')

Computing transfer functions is straightforward. First define a set of
frequency points at which to compute the response

>>> frequencies = numpy.logspace(1, 3, 10)

Next, identifying the method to compute the transfer functions depends
on what one wants to compute. For an overall, big picture of the DARM
loop, ``pydarm.darm.DARMModel`` methods can be used, e.g.,

>>> OLG = darm.compute_darm_olg(frequencies)
>>> R = darm.compute_response_function(frequencies)

More specific transfer functions are found within component
objects. For example, to compute the sensing function or actuation
function response

>>> C = darm.sensing.compute_sensing(frequencies)
>>> A = darm.actuation.compute_actuation(frequencies)

Specific transfer function methods can be found within ``pyDARM``
modules. More complex transfer functions not already defined can still
be computed by combining the transfer function methods of elements in
custom ways.

--------
Plotting
--------

>>> pydarm.plot.plot(frequencies, darm.sensing.compute_sensing,
... freq_min=1, freq_max=5000, show=True)
