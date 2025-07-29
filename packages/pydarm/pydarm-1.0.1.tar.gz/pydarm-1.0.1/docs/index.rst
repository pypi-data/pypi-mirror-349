.. pyDARM documentation master file, created by
   sphinx-quickstart on Tue Nov  8 10:12:51 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyDARM: modeling software for gravitational wave detector calibration
=====================================================================

PyDARM is the python implementation for modeling transfer functions of
the Differential Arm (DARM) servo control loop of the LIGO
gravitational wave detectors.

Using configuration files or configuration strings, a full model of the
DARM servo loop can be constructed. If only a subset of parameters are
supplied, then transfer functions using only those variables may be
calculated.

.. image:: https://badge.fury.io/py/pydarm.svg
    :target: https://badge.fury.io/py/pydarm
    :alt: pyDARM PyPI version badge
.. image:: https://img.shields.io/conda/vn/conda-forge/pydarm.svg
    :target: https://anaconda.org/conda-forge/pydarm/
    :alt: pyDARM Conda-forge version badge
.. image:: https://img.shields.io/pypi/l/pydarm.svg
    :target: https://choosealicense.com/licenses/gpl-3.0/
    :alt: pyDARM license badge
.. image:: https://img.shields.io/pypi/pyversions/pydarm.svg
    :alt: pyDARM python version badge

---------------
Getting started
---------------

.. toctree::
   :maxdepth: 1

    Installing pyDARM <install>

--------------
Using pyDARM
--------------

.. toctree::
   :maxdepth: 2

   Defining a DARM model <model/index>
   Calculating transfer functions <transferfunction/index>
   Fitting data <fitting/index>
   Gaussian process regression <unknownsys/index>
   Monitoring time dependence <timedependence/index>
   Uncertainty budget <uncertainty/index>
   Generating filters <filtering/index>

---
API
---

.. toctree::
   :maxdepth: 1

   pyDARM modules <modules>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
