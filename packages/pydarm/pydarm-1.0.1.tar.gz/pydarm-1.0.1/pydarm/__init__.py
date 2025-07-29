# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.

from . import (
    sensing,
    actuation,
    utils,
    darm,
    pcal,
    hwinj,
    # measurement,
    # uncertainty,
    plot,
    calcs,
    fir,
    firtools,
)


try:
    from ._version import version as __version__
except ModuleNotFoundError:
    try:
        import setuptools_scm
        __version__ = setuptools_scm.get_version(fallback_version='?.?.?')
    except (ModuleNotFoundError, TypeError, LookupError):
        __version__ = '?.?.?'

__author__ = 'Evan Goetz <evan.goetz@ligo.org>'
__credits__ = 'Ethan Payne, Antonios Kontos, Jameson Rollins, ' \
  'Miftahul Maarif, Afif Ismail, Hsiang-Yu Huang'
