# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ethan Payne (2020)
#               Evan Goetz (2021)
#
# This file is part of pyDARM.

import os
import configparser

import numpy as np
from scipy.signal import dfreqresp

from .analog import analog_aa_or_ai_filter_response
from .digital import iopdownsamplingfilters, daqdownsamplingfilters


# set up basic functions to check the type
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class Model(object):
    """pyDARM Model class

    Represents a transfer function.

    """
    def __init__(self, config, measurement=None):
        """Initialize Model object

        Parameters
        ----------
        config : file path or string
            INI config
        measurement : string
            measurement type, corresponding to section in the config INI

        """
        self._config = None
        self.measurement = measurement
        self._load_configuration(config)

    def _load_configuration(self, config):
        """Reads configuration and load parameters

        Config can be either file path or configuration string.
        Config interface is stored in `self._config` attribute.

        Parameters
        ----------
        config : file path or string
            INI config

        """
        if self._config is None:
            self._config = configparser.ConfigParser(
                comment_prefixes=('#',), inline_comment_prefixes=('#',),
                interpolation=configparser.ExtendedInterpolation())

        try:
            if type(config) is dict:
                self._config.read_dict(config)
            elif os.path.exists(os.path.normpath(config)):
                with open(os.path.normpath(config)) as f:
                    self._config.read_file(f)
            else:
                self._config.read_string(config)
        except Exception:
            # FIXME: expand exceptions to pass duplicate entries instead of
            # just claiming file not found.
            raise ValueError("Error parsing file", config)

        if self.measurement:
            for key, value in self._config[self.measurement].items():
                self._set_attribute(key, value)

        if 'metadata' in self._config:
            for key, value in self._config['metadata'].items():
                self._set_attribute(key, value)

        if 'interferometer' in self._config:
            for key, value in self._config['interferometer'].items():
                self._set_attribute(key, value)

    def _set_attribute(self, key, value):
        """Set Model attribute from config key/value

        """
        # Special case for module arrays
        # Sometimes (not always) keys that have the string '_modules' in their
        # name need to have a list of lists. To indicate this we use ':' in
        # the value to represent the separation of these lists
        # So, for _modules, the possibilities are:
        # - a list of 1 empty list
        # - a list of lists, where ':' separates each list
        # - a list of 1 list with values and no ':' was given in the value
        if '_modules' in key:
            if len(value) == 0:
                array = [[]]
            elif ':' in value:
                array = value.split(':')
                for index, inner_array in enumerate(array):
                    if len(inner_array) < 1:
                        inner_array = []
                    else:
                        inner_array = [
                            int(arr_entry)
                            for arr_entry in inner_array.split(',')]
                    array[index] = inner_array
            else:
                array = [[int(value_entry) for value_entry in value.split(',')]]

            value = array

        # Special case for compact measured zeros and poles of the OMC paths
        # This is like the module list of lists except instead of integers, we
        # want floats
        # - OMC paths measured zeros and poles
        elif 'omc_meas_' in key:
            # first initialize empty list of lists for the number of paths
            # determined from omc_path_names. This is required because sensing
            # methods are computed using a path name based on the list of path
            # names
            if hasattr(self, 'omc_path_names'):
                array = [[] for name in self.omc_path_names]
            elif 'omc_path_names' in self._config['sensing']:
                array = [[] for name in
                         self._config['sensing']['omc_path_names'].split(',')]
            else:
                raise KeyError('Must provide omc_path_names in [sensing]')

            # split along ':'
            for index, inner_array in enumerate(value.split(':')):
                if inner_array == '':
                    inner_array = []
                elif 'j' in inner_array:
                    inner_array = [complex(arr_entry.replace(' ', '')) for arr_entry in
                                   inner_array.split(',')]
                else:
                    inner_array = [float(arr_entry) for arr_entry in
                                   inner_array.split(',')]
                array[index] = inner_array

            value = array

        # Special case for arrays of strings that are separated by ','
        # - OMC path names
        # - OMC path analog whitening mode names
        # - sensing/pcal function anti-aliasing file names
        # - sensing/pcal function anti-aliasing rate string
        # - sensing/pcal function anti-aliasing method
        # - arm actuation function anti-imaging rate string
        # - arm actuation function anti-imaging method
        # - OMC compensation filter bank
        # - digital filter bank names
        # - OMC path compensation active
        elif (key == 'omc_path_names' or
                key == 'whitening_mode_names' or
                (self.measurement in ['sensing', 'pcal', 'electronics-measurement'] and
                 (key == 'analog_anti_aliasing_file')) or
                (self.measurement in ['sensing', 'actuation_x_arm', 'actuation_y_arm', 'pcal',
                 'electronics-measurement'] and
                 ('ing_rate_string' in key or 'ing_method' in key)) or
                ('omc_' in key and '_bank' in key) or
                key == 'digital_filter_bank' or
                (self.measurement == 'sensing' and
                 'compensation' in key)):
            value = value.strip(',')
            array = [str(value_entry).strip() for value_entry in
                     value.split(',')]

            value = array

        # Special case if the _meas_z or _meas_p values are empty
        # Aside from the OMC paths measured zeros and poles, if any other
        # measured zeros and poles are empty, then assign an empty list
        # because we don't want an empty string.
        # By using `'compensated...' in key`, this covers both "compensated"
        # and "uncompensated" keys
        elif (('compensated_z' in key and value == '') or
              ('compensated_p' in key and value == '')):
            value = []

        # Special case for the (un)compensated zeros and poles in actuation
        # These need to be in a list of floats separated by commas (,)
        elif ((self.measurement == 'actuation_x_arm' or self.measurement == 'actuation_y_arm') and
              ('compensated_z' in key or 'compensated_p' in key)):
            value.strip(',')
            if 'j' in value:
                array = [complex(value_entry.replace(' ', ''))
                         for value_entry in value.split(',')]
            else:
                array = [float(value_entry.replace(' ', ''))
                         for value_entry in value.split(',')]
            value = array

        # Special case for array of gain values (floats) separated by ','
        # where the gains need to be in a list, even if just one element
        # - sensing OMC path digital gains
        # - sensing OMC path gain ratios
        # - sensing balance matrix values
        # - sensing ADC gain values
        # - digital filter bank gain
        # - sensing OMC analog electronics apparent delay from high freq poles
        elif (('omc_' in key and '_gain' in key) or
              'gain_ratio' in key or 'balance_matrix' in key or
              key == 'adc_gain' or key == 'digital_filter_gain' or
              key == 'super_high_frequency_poles_apparent_delay'):
            value = [float(value_entry) for value_entry in value.split(',')]

        # Special case for pcal systematic error values where the values will
        # be given as LINE5=XXXX, LINE6=YYYY, etc.
        elif self.measurement == 'calcs' and 'cal_line_sys' in key:
            array = value.split(',')
            # Check that either all values contain '=' or none
            # TODO: maybe a cleaner way to do this
            if '=' in array[0]:
                for val in array:
                    if '=' not in val:
                        raise ValueError(f"'=' needs to be all values of {key} or none")
            elif '=' not in array[0]:
                for val in array:
                    if '=' in val:
                        raise ValueError(f"'=' needs to be all values of {key} or none")
            val = {}
            for idx, line in enumerate(array):
                if '=' not in line:
                    name = f'LINE{5+idx}'
                    freq = line.replace(' ', '')
                else:
                    [name, freq] = line.replace(' ', '').split('=')
                # make sure the user didn't already specify this line
                if name in val.keys():
                    raise ValueError(f'{name} and only be given once in systematic error lines')
                val[name] = float(freq)
            value = val

        # Special case for True or False as values, convert string to python
        # bool
        elif 'True' in value:
            value = True
        elif 'False' in value:
            value = False

        # Check if the value is a float
        elif isfloat(value):
            value = float(value)

        # check if the configuration entry is a 2D array
        # this is more basic than the special cases above
        elif ':' in value:
            array = value.split(':')
            for index, inner_array in enumerate(array):
                inner_array = \
                    [float(arr_entry) for arr_entry in inner_array.split(',')]
                array[index] = inner_array

            value = array

        # Check if it is a 1D array
        # this is more basic than the special cases above
        elif ',' in value:
            value = value.strip(',')
            # Check if X or Y is in the string or make floats or integers
            if ('ON' in value or 'OFF' in value or 'DARM' in value):
                array = [str(value_entry).strip()
                         for value_entry in value.split(',')]
            elif '.' in value:
                array = [float(value_entry)
                         for value_entry in value.split(',')]
            else:
                array = [int(value_entry) for value_entry in value.split(',')]

            value = array

        setattr(self, key, value)

    def dpath(self, *args):
        """Return path to data file

        Path should be relative to the directory specified in the
        `cal_data_root` configuration variable, which may be
        overridden with the CAL_DATA_ROOT environment variable.  If
        not specified, paths will be assumed to be relative to the
        current working directory.

        if os.path.join(*args) is a full path then return that.

        """
        stub = os.path.join(*args)
        if not os.path.isabs(stub):
            root = os.getenv('CAL_DATA_ROOT', getattr(self, 'cal_data_root', ''))
            stub = os.path.join(root, stub)
        return stub

    def config_to_dict(self):
        """
        Return a nested dict of the model configuration. Sections are dict
        in of themselves

        Returns
        -------
        out : dict
            dictionary of the model parameters

        """
        out = {}

        # loop over each of the sections
        for idx, val in enumerate(self._config.sections()):
            this_sect = {}

            # loop over each item in the section
            for idx2, val2 in enumerate(self._config.items(f'{val}')):
                this_sect[f'{val2[0]}'] = f'{val2[1]}'

            # add this section to the output
            out[f'{val}'] = this_sect

        return out

    def analog_aa_or_ai_filter_response(self, frequencies, idx=0):
        """
        Compute the analog anti-aliasing or anti-imaging filter response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response
        idx : `int`, optional
            if multiple files provided, use an index like 0, 1, or 2 to access
            the appropriate file (default = 0)

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the analog AA or AI filter

        """
        path = ''
        if (hasattr(self, 'analog_anti_aliasing_file') and
                getattr(self, 'analog_anti_aliasing_file') != ['']):
            path = self.analog_anti_aliasing_file[idx]
        elif hasattr(self, 'analog_anti_imaging_file'):
            path = self.analog_anti_imaging_file
        # in case the file is an empty string, we set the response to ones
        # otherwise we actually compute this
        if path == '':
            response = np.ones(len(frequencies), dtype='complex128')
        else:
            response = analog_aa_or_ai_filter_response(self.dpath(path),
                                                       frequencies)

        return response

    def digital_aa_or_ai_filter_response(self, frequencies):
        """
        Compute the digital anti-aliasing or -imaging filter response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute the response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response of the digital filter

        """

        # anti_aliasing_rate_string could be multiple strings
        if hasattr(self, 'anti_aliasing_rate_string'):
            rate_string = self.anti_aliasing_rate_string
            method = self.anti_aliasing_method
        else:
            rate_string = self.anti_imaging_rate_string
            method = self.anti_imaging_method

        response = np.ones(len(frequencies), dtype='complex128')

        for idx, this_rate_str in enumerate(rate_string):
            if this_rate_str != '':
                # Here we use a crappy 8x DAQ downsampling filter for the 512k
                # DAQ filter
                if this_rate_str == '512k-daq':
                    filt_ss = daqdownsamplingfilters(
                        524288, 65536, method[idx], rcg_ver=3)
                # RCG implementation of the 524k -> 65k (8x) IOP downsampling
                # filter
                elif this_rate_str == '524k':
                    filt_ss = iopdownsamplingfilters(
                        this_rate_str, method[idx], model_sample_rate=524288)
                else:
                    filt_ss = iopdownsamplingfilters(
                        this_rate_str, method[idx], rcg_ver=3)

                filt_zpk = filt_ss.to_zpk()

                # The 512k rate needs to be specified seprately from the 65k
                if this_rate_str == '512k-daq' or this_rate_str == '524k':
                    response *= dfreqresp(
                        filt_zpk, 2.0*np.pi*frequencies/524288)[1]
                else:
                    response *= dfreqresp(
                        filt_zpk, 2.0*np.pi*frequencies/65536)[1]

        return response
