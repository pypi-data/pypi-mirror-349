# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2021)
#
# This file is part of pyDARM.

import os
import math
import json
import multiprocessing as mp
from datetime import datetime

import h5py
import emcee
import numpy as np
from scipy.signal import freqresp, ZerosPolesGain, dfreqresp
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
import matplotlib.pyplot as plt
import dttxml
from gpstime import tconvert

from .sensing import SensingModel
from .actuation import ActuationModel
from .pcal import PcalModel
from .utils import save_chain_to_hdf5, save_gpr_to_hdf5, digital_delay_filter
from .model import Model


class Measurement(object):
    """
    This class is used to get measurement data from
    a dtt measurement. This class is used in conjuction with the
    ProcessSensingMeasurement and ProcessActuationMeasurement
    class to get the input for the MCMC and GPR analysis.

    This class uses the dttxml module to import transfer functions and ASDs.

    Parameters
    ----------
    meas_file: string
        String of the name of the xml/hdf5 file of the measurement.

    Returns
    -------

    Methods (Quick reference)
    -------
    get_raw_tf: Input two channels, get array of freq and TFs
    get_raw_asd: Input one channel, get array of freq and ASD
    get_set_of_channels: No input, get a set of the channels in meas_file.

    NOTES
    -----
    If the file is not given, the class will complain.
    """

    def __init__(self, meas_file):
        if os.path.exists(meas_file) is not True:
            raise IOError('The file given does not exist.')

        self.filename = meas_file

        # FIXME, xml only.
        # For now, I can only access the averages and gps time from the
        # file only after I get the transfer function. There must be
        # a way to get them just after we access the file. For now,
        # I just initialize them here.
        self.averages = None
        self.gps_time = None
        self.bw = None

    def get_raw_tf(self, channelA, channelB, cohThresh=0):
        """
        Given two channels it returns the transfer function from the input
        file. Note that it gives channelB/channelA.
        In addition it populates averages and gps_time, calculates the
        uncertainty from coherence, and rejects data with coherence lower
        than the given threshold.

        Parameters
        ----------
        channelA: string
            Channel in the denominator of the TF
        channelB: string
            Channel in the numerator of the TF
        cohThresh: float
            Coherence threshold below which data from dtt are rejected

        Returns
        -------
        Returns a 4 arrays N length arrays, where N is the number of data
        points:
        Array 1: frequencies (frequencies of the data in Hz)
        Array 2: tf (transfer function of B/A)
        Array 3: coh (coherence of B/A measurement)
        Array 4: unc (the uncertainty from coherence)
        """
        try:
            set_of_A_channels, set_of_B_channels = self.get_set_of_channels()
        except AttributeError:
            set_of_A_channels = set([channelA])
            set_of_B_channels = set([channelB])

        if (channelA in set_of_A_channels) and\
           (channelB in set_of_A_channels or channelB in set_of_B_channels):
            # Transfer function data holder. xfer is a method that comes from
            # dttxml. xfer takes channelB first and channelA second, which
            # is the opposite order that I am using. Whatever the ordering,
            # channelA always means the denominator and channelB is the
            # numerator. This should work for both Swept Sine
            # or FFT (aka broadband) measurements.
            if hasattr(self.data_access, 'xfer'):
                # handle dttxml data
                tf_holder = self.data_access.xfer(channelB, channelA)
                self.averages = tf_holder.averages
                self.gps_time = tf_holder.gps_second
                self.bw = tf_holder.BW
                # Frequency of the measurement in Hz
                frequencies = np.array(tf_holder.FHz)
                # Transfer function of B/A, complex array
                tf = np.array(tf_holder.xfer)
                # Coherence function of B/A, real array
                coh = np.array(tf_holder.coh)
            else:
                # handle hdf5 data
                tf_holder = self.data_access
                self.averages = np.int32(tf_holder['parameters']['averages'][()])
                self.gps_time = np.int32(min(tf_holder[channelB][channelA]['StartTimes'][()]))
                self.bw = np.float64(tf_holder['parameters']['BW'][()])
                # Frequencies stored as strings, and need to be cast to float.
                frequencies = (
                    tf_holder[channelB][channelA]['Frequencies'][()].astype(np.float64))
                tf = tf_holder[channelB][channelA]['TransferFunctions'][()]
                coh = tf_holder[channelB][channelA]['Coherences'][()]

            # Create a map that sorts by frequency, as it is not in order by design.
            indexOrder = np.argsort(frequencies)
            frequencies = frequencies[indexOrder]
            tf = tf[indexOrder]
            coh = coh[indexOrder]
            # Uncertainty from coherence
            if np.isscalar(self.averages):
                unc = np.sqrt((1.0-coh)/(2.0*(coh+1e-6)*self.averages))
            else:
                unc = np.sqrt((1.0-coh)/(2.0*(coh+1e-6)*self.averages[indexOrder]))
            # Find good coherence and intersecting points
            frequencies = frequencies[(coh > cohThresh)]
            tf = tf[(coh > cohThresh)]
            unc = unc[(coh > cohThresh)]
            coh = coh[(coh > cohThresh)]
        else:
            raise ValueError('Invalid channel for transfer function.')

        return frequencies, tf, coh, unc

    def get_raw_asd(self, channelA):
        """
        It returns the ASD of channelA from the dtt file.
        This will only work for a FFT (aka broadband) type measurement.

        Parameters
        ----------
        channelA: string
            ASD channel.

        Returns
        -------
        Returns two float array:
        Array 1: frequencies (frequencies of the data in Hz)
        Array 2: asd (ASD of channelA)
        """
        set_of_A_channels, set_of_B_channels = self.get_set_of_channels()
        if (channelA in set_of_A_channels):
            # This will only work for a FFT (aka broadband) type measurement
            asd_holder = self.data_access.asd(channelA)
            self.averages = asd_holder.averages
            self.gps_time = asd_holder.gps_second
            self.bw = asd_holder.BW
            # Frequency of the measurement in Hz
            frequencies = np.array(asd_holder.FHz)
            # Amplitude Spectral Density of requested channel
            asd = np.array(asd_holder.asd)
            return frequencies, asd
        else:
            raise ValueError('Invalid channel for asd.')

    def get_set_of_channels(self):
        """
        Method to get the channels in the measurement file.
        Annoyingly, the channels are given in a set.

        For the .hdf5, channels can be swapped around freely, returing the inverse as
        expected.
        Parameters
        ----------

        Returns
        -------
        channels_A: A python set with all the A channels in the measurement
        file of this object.
        channels_B: A python set with all the B (NON-A) channels in the
        measurement file of this object.
        """
        if hasattr(self.data_access, 'channels'):
            channels_A, channels_B = self.data_access.channels()
        else:
            channels_A, channels_B = \
                    set(np.array(self.data_access['parameters']['channelA'][()]).astype(str)), \
                    set(np.array(self.data_access['parameters']['channelB'][()]).astype(str))
            channels_B = channels_B - channels_A
        return channels_A, channels_B

    @property
    def data_access(self):
        # Data accessing object. It is called later.
        meas_file = self.filename
        base, ext = os.path.splitext(meas_file)
        if ext == '.xml':
            data_access = dttxml.DiagAccess(meas_file)
        elif ext == '.hdf5':
            data_access = h5py.File(meas_file, 'r')
        else:
            raise TypeError('Invalid file type input.')
        return data_access


class ProcessOneMeasurement(object):
    """
    This class is used in conjuction with measurement data and ouputs
    arrays used in general use

    Parameters
    ----------
    config_file : `str`
        This is the *.ini model file to be used to process the measurement data
    meas : `Measurement`
        This is the object that contains the data for either the closed
        loop gain (sensing measurement) or suspension measurement (actuation)
    meas_tup : `str`, tuple
        This should be ('channel A', 'channel B') for the first measurement
    meas_cohThresh : `float`, optional
        Coherence threshold that values in measurement must be above to be
        included; valid values in the range [0,1]. (default = 0)

    """

    def __init__(self, config_file, meas, meas_tup, meas_cohThresh=0):
        if len(meas_tup) != 2:
            raise ValueError('Invalid string tuple for meas_tup')
        if meas_cohThresh < 0.0 or meas_cohThresh > 1.0:
            raise ValueError('meas1_cohThresh must be in range [0,1]')

        self.config_file = os.path.abspath(config_file)
        self.measurement = meas
        self.meas_tup = meas_tup
        self.meas_cohThresh = meas_cohThresh

    def pre_process_transfer_functions(self):
        """
        This method extracts the transfer function data using the channel names
        from the DTT files specified in the object and computes the
        intermediate data products by removing known parameters
        (see G1501518-v21).

        Returns
        -------
        frequencies : `float`, array-like
            frequency values of the transfer function, in units of Hz
        tf_meas : `complex128`, array-like
            the extracted transfer function from meas_tup_1, excluding
            frequency points below the meas1_cohThresh coherence threshold
        unc_meas : `float`, array-like
            relative uncertainty of measurement data

        """

        freq_meas, tf_meas, coh_meas, unc_meas = \
            self.measurement.get_raw_tf(self.meas_tup[0],
                                        self.meas_tup[1],
                                        self.meas_cohThresh)

        return freq_meas, \
            tf_meas, coh_meas, unc_meas


class ProcessMeasurement(object):
    """
    This class is used in conjuction with measurement data and ouputs
    arrays used as input to MCMC and GPR routines.
    For reference, please see G1501518-v21 subway map, and specifically
    'MCMC input for C' or 'MCMC input for A'.

    Parameters
    ----------
    config_file : `str`
        This is the *.ini model file to be used to process the measurement data
    meas_sensing_or_actuation : `Measurement`
        This is the object that contains the data for either the closed
        loop gain (sensing measurement) or suspension measurement (actuation)
    meas_pcal_to_darm : `Measurement`
        This is the object that contains data for the PCAL to DARM TF
    meas_tup_1 : `str`, tuple
        This should be ('channel A', 'channel B') for the first measurement
    meas_tup_2 : `str`, tuple
        This should be ('channel A', 'channel B') for the second measurement
    meas1_cohThresh : `float`, optional
        Coherence threshold that values in measurement 1 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    meas2_cohThresh : `float`, optional
        Coherence threshold that values in measurement 2 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    json_results_file : `str`, optional
        Filename for a JSON file

    """

    def __init__(self, config_file, meas_sensing_or_actuation, meas_pcal_to_darm,
                 meas_tup_1, meas_tup_2, meas1_cohThresh=0, meas2_cohThresh=0,
                 json_results_file=None):
        if len(meas_tup_1) != 2:
            raise ValueError('Invalid string tuple for meas_tup_1')
        if len(meas_tup_2) != 2:
            raise ValueError('Invalid string tuple for meas_tup_2')
        if meas1_cohThresh < 0.0 or meas1_cohThresh > 1.0:
            raise ValueError('meas1_cohThresh must be in range [0,1]')
        if meas2_cohThresh < 0.0 or meas2_cohThresh > 1.0:
            raise ValueError('meas2_cohThresh must be in range [0,1]')

        self.PCAL = PcalModel(config_file)
        self.config_file = os.path.abspath(config_file)
        self.measurement_1 = meas_sensing_or_actuation
        self.measurement_2 = meas_pcal_to_darm
        self.meas_tup_1 = meas_tup_1
        self.meas_tup_2 = meas_tup_2
        self.meas1_cohThresh = meas1_cohThresh
        self.meas2_cohThresh = meas2_cohThresh
        self.json_results_file = json_results_file

        self.endstation = False
        if 'CAL-DELTAL_REF_PCAL' not in self.meas_tup_2[0]:
            self.endstation = True

    def pre_process_transfer_functions(self):
        """
        This method extracts the transfer function data using the channel names
        from the DTT files specified in the object and computes the
        intermediate data products by removing known parameters
        (see G1501518-v21).

        Returns
        -------
        frequencies : `float`, array-like
            frequency values of the transfer function, in units of Hz
        tf_meas1 : `complex128`, array-like
            the extracted transfer function from meas_tup_1, excluding
            frequency points below the meas1_cohThresh coherence threshold
        tf_meas2 : `complex128`, array-like
            the extracted transfer function from meas_tup_2, excluding
            frequency points below the meas2_cohThresh coherence threshold
        pcal_correction : `complex128`, array-like
            the transfer function for the offline photon calibrator correction
        processed_measurement_response_unc : `float`, array-like
            relative uncertainty of combined measurement data

        """

        freq_meas1, tf_meas1, coh_meas1, unc_meas1 = \
            self.measurement_1.get_raw_tf(self.meas_tup_1[0],
                                          self.meas_tup_1[1],
                                          self.meas1_cohThresh)
        freq_meas2, tf_meas2, coh_meas2, unc_meas2 = \
            self.measurement_2.get_raw_tf(self.meas_tup_2[0],
                                          self.meas_tup_2[1],
                                          self.meas2_cohThresh)

        # Merge common frequency elements from the two transfer functions.
        # Here we could have used the numpy.isin function, but there are no
        # tolerance options. It appears there may be some desire for a
        # tolerance (from other measurements), but if this is not a desireable
        # features, it could be reverted
        mask_1 = _isin(freq_meas1, freq_meas2, abs_tol=1e-3)
        mask_2 = _isin(freq_meas2, freq_meas1, abs_tol=1e-3)

        freq_meas1 = freq_meas1[mask_1]
        tf_meas1 = tf_meas1[mask_1]
        coh_meas1 = coh_meas1[mask_1]
        unc_meas1 = unc_meas1[mask_1]

        freq_meas2 = freq_meas2[mask_2]
        tf_meas2 = tf_meas2[mask_2]
        coh_meas2 = coh_meas2[mask_2]
        unc_meas2 = unc_meas2[mask_2]

        if np.allclose(freq_meas1, freq_meas2):
            frequencies = freq_meas2
        else:
            raise ValueError('Something went wrong with matching the ',
                             'frequencies of the two transfer functions')

        if len(frequencies) < 1:
            raise ValueError('There are no common frequency points for the ',
                             'two transfer functions. Maybe check coherence',
                             ' thresholds.')

        pcal_correction = self.PCAL.compute_pcal_correction(frequencies,
                                                            self.endstation)

        processed_measurement_response_unc = np.sqrt(unc_meas1**2
                                                     + unc_meas2**2)

        return frequencies, \
            tf_meas1, tf_meas2, pcal_correction, \
            processed_measurement_response_unc

    def crop_data(self, xdata, ydata, yerr, fmin=None, fmax=None):
        """
        Crop the data with optional minimum and maximum bounds

        Parameters
        ----------
        xdata : `float`, array-like
            Original frequency data
        ydata : `complex`, array-like
            Original transfer function data
        yerr : `float`, array-like
            Original uncertainties computed from the coherence values
        fmin : `float`, optional
            Optional minimum frequency value for the MCMC fitting. Default is
            the minimum frequency of xdata (default = None)
        fmax : `float`, optional
            Optional maximum frequency value for the MCMC fitting. Default is
            the maximum frequency of xdata (default = None)

        Returns
        -------
        xdata : `float`, array-like
            cropped frequencies
        ydata : `complex`, array-like
            cropped transfer function data
        yerr : `float`, array-like
            cropped uncertainties computed from the coherence values

        """
        # Mask the data the is within the frequency band selected by the user
        if fmin is not None and fmax is not None:
            xdata_mask = np.ma.masked_inside(xdata, fmin, fmax)
        elif fmin is not None and fmax is None:
            xdata_mask = np.ma.masked_greater_equal(xdata, fmin)
        elif fmin is None and fmax is not None:
            xdata_mask = np.ma.masked_less_equal(xdata, fmax)
        else:
            xdata_mask = np.ma.masked_array(xdata)
            xdata_mask.mask = True
        xdata = xdata[xdata_mask.mask]
        ydata = ydata[xdata_mask.mask]
        yerr = yerr[xdata_mask.mask]

        return xdata, ydata, yerr

    def _mcmc(self, xdata, ydata, yerr, priors, priors_bound,
              burn_in_steps=1000, steps=9000):
        """
        Run an MCMC over the processed measurement data

        Parameters
        ----------
        xdata : `float`, array-like
            Frequency values array
        ydata : `complex`, array-like
            Transfer function data corresponding to the frequency array
        yerr : `float`, array-like
            Absolute error values for each transfer function measurement point
        priors : `float`, array-like
            An N x M array of initial values where N is the
            number of walkers and M is the number of parameters
        priors_bound : `float`, array-like
            User-specified boundary of prior distribution, a M x 2
            array where the first (second) element of each row
            corresponds to the lower (upper) bound of each parameter
        burn_in_steps : `int`, optional
            Number of steps in the burn-in phase of the MCMC (default = 1000)
        steps : `int`, optional
            Number of steps in the main phase of the MCMC (default = 9000)

        Returns
        -------
        chain : `float`, array-like
            The results of the MCMC chain

        """

        # Set the numpy parallelization to a single thread because
        # emcee has said this can cause problems
        os.environ['OMP_NUM_THREADS'] = '1'

        global xdata_gl, ydata_gl, yerr_gl
        xdata_gl, ydata_gl, yerr_gl = xdata, ydata, yerr

        # Use multiprocessing to run the MCMC faster
        # Using this instead of "with Pool() as pool:"
        # See pyDARM issue #47 for the reason for this change
        with mp.get_context('fork').Pool() as pool:
            sampler = emcee.EnsembleSampler(len(priors[:, 0]),
                                            len(priors[0, :]),
                                            _ln_prob,
                                            pool=pool,
                                            kwargs={'bound': priors_bound})
            # This is burn-in, but I wonder if there is a better way to do
            # this using the v3 of emcee. There are some optional arguments
            # when calling like 'flat','thin','discard'
            pos, prob, state = sampler.run_mcmc(priors, burn_in_steps,
                                                progress=True)
            sampler.reset()

            # Now running the actual sampling
            sampler.run_mcmc(pos, steps, progress=True)

        # I've been told by some MCMC experts that one should thin the
        # chain, but the autocorr time seems quite long, meaning we'd thin
        # the chain quite a lot unless we run a much longer MCMC chain
        # So right now we don't do any thinning
        # print(sampler.get_autocorr_time(tol=10, quiet=True))

        # Return back to normal numpy operation by unsetting the environment
        os.unsetenv('OMP_NUM_THREADS')

        # Return the array of MCMC samples
        return sampler.get_chain(flat=True)

    def save_results_to_json(self, filename, fmin, fmax, mcmc_map_vals, measurement, append=False):
        """
        Save the model, input DTT filenames, coherence threshold values,
        minimum and maximum frequencies used in the MCMC, and the resulting
        MCMC MAP values

        Parameters
        ----------
        filename : str
            path and file name to JSON file
        fmin : float
            minimum frequency used for the MCMC
        fmax : float
            maximum frequency used for the MCMC
        mcmc_map_vals : `float`, array-like
            array of maximum a postiori values found from the MCMC
        measurement : str
            measurement type; one of 'sensing', 'actuation_x_arm', or 'actuation_y_arm'
        append : bool
            if True, append results to existing JSON file, otherwise overwrite

        """
        # Prepare the new dict for the JSON archive
        now = datetime.now()

        if measurement == 'sensing':
            config_dict = self.sensing.config_to_dict()
        elif (measurement == 'actuation_x_arm' or measurement == 'actuation_y_arm'):
            config_dict = self.actuation.config_to_dict()
        else:
            raise ValueError('Neither actuation nor sensing was provided')

        measurement_info = {'Measurement analysis {}'.format(
            now.strftime('%d/%m/%Y %H:%M:%S')): {
            'model_config_file': str(self.config_file),
            'meas_type': measurement,
            'model_config': config_dict,
            'loop_meas': str(self.measurement_1.filename),
            'pcal_meas': str(self.measurement_2.filename),
            'loop_tup': self.meas_tup_1,
            'pcal_tup': self.meas_tup_2,
            'loop_cohthresh': self.meas1_cohThresh,
            'pcal_cohthresh': self.meas2_cohThresh,
            'fmin': fmin, 'fmax': fmax,
            'mcmc_map_vals': mcmc_map_vals.tolist()}}

        # Either read in and make an addition to the JSON archive or create
        # the file if it didn't exist
        filename = os.path.normpath(filename)
        if os.path.exists(filename) and append is True:
            # JSON doesn't like to read/write files in append mode for some
            # reason
            with open(filename, 'r') as f:
                data = json.load(f)
            data.update(measurement_info)
            with open(filename, 'w') as f:
                json.dump(data, f)
        else:
            with open(filename, 'w') as f:
                json.dump(measurement_info, f)

        return

    def query_results_from_json(self, measurement, fmin=None, fmax=None,
                                match='latest', strict=False):
        """
        Query the JSON file for MCMC results. The query looks in the JSON
        file for a matching set of measurement files, configuration,
        coherence thresholds, and--optionally--the minimum and maximum
        frequency of the fit. `match` will determine what to return.
        It can be 'first' for the first matched, 'latest' for the last matched,
        'all' for all matched or specify which result to return by providing
        the date of measurement analysis 'DD/MM/YYYY HH:MM:SS'

        Parameters
        ----------
        measurement : str
            measurement type; one of 'sensing' or 'actuation'
        fmin : `float`, optional
            minimum frequency used for the MCMC
        fmax : `float`, optional
            maximum frequency used for the MCMC
        match : `str`, optional
            result to return; 'first', 'latest', 'all' or
            the date of measurement analysis 'DD/MM/YYYY HH:MM:SS'
        strict : `bool`, optional
            if True, return the first entry in the json file. Default is False.

        Returns
        -------
        measurement analysis date : `str`
            the date of processing measurement analysis in form of 'DD/MM/YYYY HH:MM:SS'
        mcmc_map_vals : `float`, array-like
            array of maximum a postiori values found from the MCMC
        is_pro_spring : bool
            parameter for whether the fit assumed anti-spring (False) or
            pro-spring (True)

        """

        # Load the data from the specified JSON file
        json_results_file = os.path.normpath(self.json_results_file)
        with open(json_results_file, 'r') as f:
            data = json.load(f)

        if strict is False:
            # grab first entry in json file
            key = list(data.keys())[0]
            this_date = key[21:]  # there must be a better way to get date, L.D.
            this_map = np.asarray(data[key]['mcmc_map_vals'])
            data_spring = data[key]['model_config']['sensing']['is_pro_spring']
            this_spring = True if data_spring == 'True' else False
            output = [this_date, this_map, this_spring]

        else:
            # Loop through the analyis entries, looking for only the results with
            # input values that match the request. If there are any mismatches,
            # then the loop breaks early and no result is returned
            query_match = ''
            output = []
            for idx, key in enumerate(data):
                for idx2, (key2, val2) in enumerate(data[key].items()):
                    if (key2 == 'loop_meas' and
                        os.path.basename(val2) != os.path.basename(
                            self.measurement_1.filename)):
                        break
                    if (key2 == 'pcal_meas' and
                        os.path.basename(val2) != os.path.basename(
                            self.measurement_2.filename)):
                        break
                    if key2 == 'loop_cohthresh' and val2 != self.meas1_cohThresh:
                        break
                    if key2 == 'pcal_cohthresh' and val2 != self.meas2_cohThresh:
                        break
                    if fmin is not None and key2 == 'fmin' and val2 != fmin:
                        break
                    if fmax is not None and key2 == 'fmax' and val2 != fmax:
                        break
                    if key2 == 'model_config':
                        # copy the sensing models because we want to pop off
                        # parameters associated with coupled_cavity and
                        # detuned_spring because those will be assocaited with
                        # MCMC values
                        if measurement not in val2:
                            break

                        json_model = val2[measurement].copy()
                        if measurement == 'sensing':
                            this_model = \
                                self.sensing.config_to_dict()[measurement]
                        else:
                            this_model = \
                                self.actuation.config_to_dict()[measurement]
                        this_model_copy = this_model.copy()

                        for idx3, (key3, val3) in enumerate(
                                val2[measurement].items()):
                            if ('coupled_cavity' in key3 or
                                    'detuned_spring' in key3 or
                                    '_NpA' in key3 or '_NpV2' in key3):
                                json_model.pop(key3)
                        for idx3, (key3, val3) in enumerate(
                                this_model_copy.items()):
                            if ('coupled_cavity' in key3 or
                                    'detuned_spring' in key3 or
                                    '_NpA' in key3 or '_NpV2' in key3):
                                this_model.pop(key3)
                        if (val2['pcal'] != self.PCAL.config_to_dict()['pcal'] or
                                json_model != this_model):
                            break
                    if key2 == 'mcmc_map_vals':
                        continue
                    pass
                if idx2 == len(data[key])-1:
                    query_match = key

                    if measurement == 'sensing':
                        # FIXME: is_pro_spring is populated with "1" in .json map file
                        # this block compares against string 'True'. this may be a bug.
                        is_pro_spring = \
                            data[query_match]['model_config']['sensing']['is_pro_spring']
                        if is_pro_spring == 'True':
                            is_pro_spring = True
                        else:
                            is_pro_spring = False
                    else:
                        is_pro_spring = None

                    output.append([key[21:], np.asarray(data[query_match]['mcmc_map_vals']),
                                   is_pro_spring])

                if query_match[21:] == match:
                    output = output[-1]
                    break
                if match == 'first' and len(output) != 0:
                    break

            if match == 'latest':
                output = output[-1]

            if match != 'latest' and match != 'first' and match != 'all' \
               and query_match[21:] != match:
                raise ValueError(
                    'Need to choose what to return: first, latest, '
                    'all, or measurement analysis date')

            if query_match == '':
                raise ValueError(
                    'No results in the JSON archive match query values')

        return output

    def stack_measurements(self):
        """ This method is meant to be overloaded by inherited classes """

        raise Exception('This method is intended to be overloaded by child'
                        'classes')

    def _gpr(self, freq, meas_list, fmin, fmax, fmin_list, fmax_list,
             RBF_length_scale, RBF_length_scale_limits, gpr_flim,
             strict_stack=False, roaming_measurement_list_x=None,
             roaming_measurement_list_y=None):
        """
        Run a GPR over the processed measurement data

        Parameters
        ----------
        freq : `float`, array-like
            Frequencies at which to compute the GPR (Hz)
        residuals : `complex128`, array-like
            residuals of the list of measurements
        RBF_length_scale : `float`
            Initial length scale guess for the RBF term of the GPR fit (in logarithmic frequency)
        RBF_length_scale_limits : pair of floats >= 0
            The lower and upper bound on RBF_length_scale

        Returns
        -------
        y_pred : `complex128`, array-like
            Best fit curve using the GPR and covariance kernel
        sigma : `float`, array-like
            Standard deviation for the GPR
        cov : `float`, array-like
            Covariance matrix for the GPR
        stacked_meas : `list`, array-like
            list of stacked measurement frequencies, transfer functions,
            rescaled transfer functions (to reference), uncertainties, and
            residuals
        tdcfs : list
            list of time dependent correction factors for each measurement

        """

        stacked_meas, tdcfs = self.stack_measurements(
            meas_list, fmin, fmax,
            fmin_list, fmax_list,
            strict=strict_stack,
            roaming_measurement_list_x=roaming_measurement_list_x,
            roaming_measurement_list_y=roaming_measurement_list_y)

        for idx, this_meas in enumerate(stacked_meas):
            # Create a mask array where True means the data values should be
            # ignored while False indicates the data should be included
            if gpr_flim is not None:
                mask = np.ma.masked_outside(
                    this_meas[0], gpr_flim[0], gpr_flim[1])
                mask = np.ma.getmaskarray(mask)
            else:
                mask = np.array([False] * len(this_meas[0]))

            # Create / append to an array of frequencies, residuals, and
            # uncertainties
            if idx == 0:
                residuals = np.array(
                    [this_meas[0][~mask],
                     this_meas[4][~mask],
                     this_meas[3][~mask]]).T
            else:
                residuals = np.vstack(
                    (residuals, np.array(
                        [this_meas[0][~mask],
                         this_meas[4][~mask],
                         this_meas[3][~mask]]).T))

        # Now clean up, extract, and get in the right shape for the GPR
        fdata = np.log10(np.real(residuals[None, :, 0].T))
        meas = np.hstack((np.real(residuals[None, :, 1].T), np.imag(residuals[None, :, 1].T)))
        unc = np.real(residuals[None, :, 2])

        # Gaussian process regression
        # kernel, we are still using kernel for O3
        kernel = ConstantKernel(0.5, (0.1, 2.0)) * RBF(RBF_length_scale, RBF_length_scale_limits) \
            + ConstantKernel(1.0, (0.9, 1.1))

        # Fit to data using Maximum Likelihood Estimation of the parameters
        gp = GaussianProcessRegressor(kernel=kernel, alpha=unc, n_restarts_optimizer=10)
        gp.fit(fdata, meas)

        # Make the prediction
        y_pred, sigma = gp.predict(np.log10(freq[None, :].T), return_std=True)
        y_pred, cov = gp.predict(np.log10(freq[None, :].T), return_cov=True)
        y_pred = y_pred[:, 0] + 1j*y_pred[:, 1]

        # Remove 2nd feature standard deviation and covariance contribution.
        # Since the GP fits real and imaginary as two features with the identical
        # uncertainties, the inferred covariance matrices have identical structure.
        # So we need to simply throw the second feature's identical uncertainty away.
        # This requires scikit-learn > 1.0.2.

        sigma = sigma[:, 0]
        cov = cov[:, :, 0]

        return y_pred, sigma, cov, stacked_meas, tdcfs, gp


class ProcessSensingMeasurement(ProcessMeasurement):
    """
    This class is used in conjuction with measurement data and ouputs
    arrays used as input to MCMC and GPR routines.
    For reference, please see G1501518-v21 subway map, and specifically
    'MCMC input for C'.

    Parameters
    ----------
    config_file : `str`
        This is the *.ini model file to be used to process the measurement data
    meas_clg : `Measurement`
        This is the object that contains the data for the closed loop gain
    meas_pcal_to_darm : `Measurement`
        This is the object that contains data for the PCAL to DARM TF
    meas_tup_1 : `str`, tuple
        This should be ('channel A', 'channel B') for the first measurement
        Ex.: ('H1:LSC-DARM1_IN2', 'H1:LSC-DARM1_EXC')
    meas_tup_2 : `str`, tuple
        This should be ('channel A', 'channel B') for the second measurement
        Ex.: ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ')
    meas1_cohThresh : `float`, optional
        Coherence threshold that values in measurement 1 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    meas2_cohThresh : `float`, optional
        Coherence threshold that values in measurement 2 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    json_results_file : `str`, optional
        Filename of a JSON file when stacking measurements or running GPR

    """

    def __init__(self, config_file, meas_clg, meas_pcal_to_darm, meas_tup_1,
                 meas_tup_2, meas1_cohThresh=0, meas2_cohThresh=0,
                 json_results_file=None):
        super().__init__(config_file, meas_clg, meas_pcal_to_darm,
                         meas_tup_1, meas_tup_2, meas1_cohThresh,
                         meas2_cohThresh, json_results_file)
        self.sensing = SensingModel(config_file)
        self.meas_type = 'sensing'

    def get_processed_measurement_response(self):
        """
        This method extracts the transfer function data using the channel names
        from the DTT files specified in the object and computes the measurement
        response by removing known parameters (see G1501518-v21).

        Returns
        -------
        frequencies : `float`, array-like
            frequency values of the transfer function, in units of Hz
        processed_measurement_response : `complex128`, array-like
            transfer function response of the actuation function in units
            of digital counts per meter of DARM
        processed_measurement_response_unc : `float`, array-like
            relative uncertainty of processed measurement data

        """

        # First get the intermediate data products from the measurement
        (frequencies, tf_meas1, tf_meas2, pcal_correction,
         processed_measurement_response_unc) = \
            self.pre_process_transfer_functions()

        # For the sensing function correction, we need the known terms
        tf_meas1_correction = \
            self.sensing.sensing_residual(frequencies)

        # Now bring everything together; see G1501518
        processed_measurement_response = \
            tf_meas1 * tf_meas2 / (tf_meas1_correction * pcal_correction)

        return (frequencies,
                processed_measurement_response,
                processed_measurement_response_unc)

    def rescale_sensing_by_tdcf_vals(self, frequencies, response,
                                     kappa_c=1.0, f_cc=None, **kwargs):
        """
        This method rescales the response function by dividing out the kappa_c
        and frequency response of the f_cc value and multiplying in the
        reference values given in the configuration file

        Parameters
        ----------
        frequencies : `float`, array-like
            Frequency values for the transfer functions
        response : `complex128`, array-like
            Transfer function of the optical response, having divided out the
            known quantities from the measured transfer functions
        kappa_c : `float`, optional
            The time dependent correction factor for optical gain for this
            measurement. The data is divided by this number, so if anything
            other than the default value is provided, the data will be scaled
            differently (default = 1)
        f_cc : `float`, optional
            If provided, this coupled-cavity pole frequency transfer function
            will be divided out from the data and the reference value provided
            in the configuration file will be multiplied in (default = None)

        Returns
        -------
        response : `complex128`, array-like
            The scaled transfer function of optical response

        """

        # Important note: the attribute for SensingModel are actually all
        # lowercase values. So in the ini file, if you have detuned_spring_Q
        # it is actually stored in the object as detuned_spring_q
        if f_cc is not None:
            this_response_zpk = \
                SensingModel.optical_response(
                    f_cc, self.sensing.detuned_spring_frequency,
                    self.sensing.detuned_spring_q, self.sensing.is_pro_spring)
            ref_response_zpk = \
                SensingModel.optical_response(
                    self.sensing.coupled_cavity_pole_frequency,
                    self.sensing.detuned_spring_frequency,
                    self.sensing.detuned_spring_q,
                    self.sensing.is_pro_spring)
            this_response = freqresp(this_response_zpk,
                                     2.0*np.pi*frequencies)[1]
            ref_response = freqresp(ref_response_zpk,
                                    2.0*np.pi*frequencies)[1]
            response *= ref_response / this_response

        response *= 1.0 / kappa_c

        return response

    def run_mcmc(self, fmin=None, fmax=None, priors_bound=None,
                 save_map_to_file=None, save_chain_to_file=None, **kwargs):
        """
        This method is what is used to process the sensing function measurement
        data

        Parameters
        ----------
        fmin : `float`, optional
            Optional minimum frequency value for the MCMC fitting. Default is
            the minimum frequency of xdata (default = None)
        fmax : `float`, optional
            Optional maximum frequency value for the MCMC fitting. Default is
            the maximum frequency of xdata (default = None)
        priors_bound: `float`, array-like, optional
            User-specified boundary of prior distribution. Default boundaries
            are only for spring freq (must be within this range
            0.0<spring freq<20.0) and inv Q (must be within this range
            1.e-2<inv Q<1.0).
            If choosing a different set of boundaries, then this argument
            should be in form of a 2D array, 5X2. First (second) element of
            each row corresponds to the lower (upper) bound of each
            parameters: gain, pole freq, spring freq, inv Q, residual delay.
        save_map_to_file : `str`, optional
            Filename (JSON) to save the maximum a postiori values from this
            result
        save_chain_to_file : `str`, optional
            Filename (HDF5) to save the postirior chain from this result
        kwargs : optional
            other kwargs are passed to ProcessMeasurement._mcmc

        Returns
        -------
        chain : `float`, array-like
            The MCMC chain where index:
            - 0 is the gain in units of counts per meter of DARM
            - 1 is the coupled cavity pole frequency in units of Hz
            - 2 is the optical spring frequency in units of Hz
            - 3 is the quality factor of the optical spring (Q, unitless)
            - 4 is the residual time delay in units of seconds

        """
        global meas_type_gl, is_pro_spring_gl, include_spring_gl
        meas_type_gl = self.meas_type
        is_pro_spring_gl = self.sensing.is_pro_spring

        if (hasattr(self.sensing, 'include_spring') and
                getattr(self.sensing, 'include_spring') != ''):
            # Just in case, be extra sure that we pass a boolean
            include_spring_gl = bool(self.sensing.include_spring)
        else:
            # default to True if nothing given
            include_spring_gl = True

        (frequencies, processed_measurement_response,
         processed_measurement_response_unc) = \
            self.get_processed_measurement_response()

        # For the MCMC, we need to use the absolute error and not the relative
        # uncertainty
        processed_measurement_response_err = \
            processed_measurement_response_unc * \
            np.abs(processed_measurement_response)

        # crop data used in the MCMC
        xdata, ydata, yerr = self.crop_data(frequencies,
                                            processed_measurement_response,
                                            processed_measurement_response_err,
                                            fmin, fmax)

        # priors
        nwalkers = 1000
        if priors_bound is not None:
            sensing_mag = (priors_bound[0][1] + priors_bound[0][0]) / 2
            gain_sigma = (priors_bound[0][1] - priors_bound[0][0]) / np.sqrt(12)
            f_cc_mean = (priors_bound[1][1] + priors_bound[1][0]) / 2
            f_cc_sigma = (priors_bound[1][1] - priors_bound[1][0]) / np.sqrt(12)
            f_s_min = priors_bound[2][0]
            f_s_max = priors_bound[2][1]
            inv_Q_min = priors_bound[3][0]
            inv_Q_max = priors_bound[3][1]
            residual_delay_min = priors_bound[4][0]
            residual_delay_max = priors_bound[4][1]
        else:
            sensing_mag = np.max(np.abs(ydata))
            gain_sigma = 0.3 * sensing_mag
            f_cc_mean = 400.0
            f_cc_sigma = 0.1 * f_cc_mean
            f_s_min = 1
            f_s_max = 10
            inv_Q_min = 0.01
            inv_Q_max = 0.05
            residual_delay_min = -61e-6
            residual_delay_max = 61e-6
        priors = np.hstack((
            np.random.normal([sensing_mag, f_cc_mean],
                             [gain_sigma, f_cc_sigma],
                             size=(nwalkers, 2)),
            np.random.uniform([f_s_min, inv_Q_min, residual_delay_min],
                              [f_s_max, inv_Q_max, residual_delay_max],
                              size=(nwalkers, 3))))

        chain = self._mcmc(xdata, ydata, yerr, priors, priors_bound, **kwargs)

        if not include_spring_gl:
            chain[:, 2] = np.zeros(len(chain[:, 0]))
            chain[:, 3] = 1e-3 * np.ones(len(chain[:, 0]))

        # Fix 1/Q ==> Q
        chain[:, 3] = 1/chain[:, 3]

        if save_map_to_file is not None:
            self.save_results_to_json(
                save_map_to_file, fmin, fmax, np.median(chain, axis=0),
                self.meas_type)

        if save_chain_to_file is not None:
            save_chain_to_hdf5(
                save_chain_to_file, self.sensing.config_to_dict(), fmin, fmax,
                self.meas_type, chain)

        return chain

    def inverse_sensing_foton_filter(self, mcmc_chain):
        """
        Prints the FOTON filter string to the terminal. Would be preferable
        at some point if this could be automatically put in to the correct
        FOTON filter file, but at present this capability is not available

        Parameters
        ----------
        mcmc_chain : `float`, array-like
            The result from the run_mcmc() method

        """

        MAP_values = np.median(mcmc_chain, axis=0)

        if not self.sensing.is_pro_spring:
            # Take s^2/(s^2 + s0^2 - i*s*s0/Q) and solve denominator for zeros
            # fs for FOTON is abs(1/(2*pi*i)*s') where s' are the two solutions
            # to the quadratic formula - see alog LHO 31693
            fs1 = (1.0/(2.0*np.pi) *
                   (-2.0*np.pi*MAP_values[2]/MAP_values[3]/2.0 +
                    0.5*np.sqrt((2.0*np.pi*MAP_values[2]/MAP_values[3])**2 +
                                4.0*(2.0*np.pi*MAP_values[2])**2)))
            fs2 = (1.0/(2.0*np.pi) *
                   (-2.0*np.pi*MAP_values[2]/MAP_values[3]/2.0 -
                    0.5*np.sqrt((2.0*np.pi*MAP_values[2]/MAP_values[3])**2 +
                                4.0*(2.0*np.pi*MAP_values[2])**2)))
        else:
            # Take s^2/(s^2 - s0^2 + i*s*s0/Q) and solve denominator for zeros
            Real = MAP_values[2]/2.0/MAP_values[3]
            Imag = (MAP_values[2]/2.0/MAP_values[3] *
                    np.sqrt(4.0*MAP_values[3]**2-1))
            fs1 = Real + Imag*1j
            fs2 = Real - Imag*1j

        # Correct normalization
        # Make a ZPK filter that is the inverse of the single pole model
        # This means the cavity pole will become a zero
        # To keep the filter constrained, we include an artificial pole at
        # 7 kHz
        singlepolefilt = ZerosPolesGain(-2.0*np.pi*MAP_values[1],
                                        -2.0*np.pi*7000.0,
                                        7000.0/MAP_values[1])
        # We want the filter normalized at 500 Hz
        normalization_value_at_500Hz = \
            abs(freqresp(singlepolefilt, 2.0*np.pi*500.0)[1][0])
        # Now compute a ZPK filter that is the inverse of the optical response
        # by including the cavity pole and (anti-)spring. To keep the filter
        # constrained, we include two poles at 0.1 Hz and one pole at 7 kHz
        modelfilt = \
            ZerosPolesGain(
                -2.0*np.pi*np.array([MAP_values[1], fs1, fs2]),
                -2.0*np.pi*np.array([0.1, 0.1, 7000]),
                np.prod(-2.0*np.pi*np.array([0.1, 0.1, 7000.0])) /
                np.prod(-2.0*np.pi*np.array([MAP_values[1], fs1, fs2])))
        # The gain is the ratio of the single pole gain to the complete optical
        # response at 500 Hz
        gainval = normalization_value_at_500Hz / \
            abs(freqresp(modelfilt, 2.0*np.pi*500.0)[1][0])

        # Print output FOTON filter
        out = 'Inverse Sensing FOTON values: '
        out += '[NB: SRCD2N zpk gain based on sensing sign in parameters '
        out += 'file]\n'
        if not self.sensing.is_pro_spring:
            out += f'SRCD2N: zpk([{MAP_values[1]:.4f};'
            out += f'{fs1:.4f};{fs2:.4f}],[0.1;0.1;7000],'
            out += f'{self.sensing.sensing_sign:.0f},"n")'
            out += f'gain({gainval:.2f})\n'
        else:
            out += f'SRCD2N: zpk([{MAP_values[1]:.4f};'
            out += f'{Real:.4f}+i*{Imag:.4f};{Real:.4f}-i*{Imag:.4f}],'
            out += f'[0.1;0.1;7000],{self.sensing.sensing_sign:.0f},"n")'
            out += f'gain({gainval:.2f})\n'
        out += f'Gain: gain({1/MAP_values[0]:.4g})\n\n'

        # Need to print a FOTON filter that has no cavity pole and no 7000 Hz
        # filter for the CFTD path
        out += 'Inverse Sensing without cavity pole FOTON values '
        out += 'for CFTD path: [NB: SRCD2N zpk gain based on sensing sign '
        out += 'in parameters file]\n'
        if not self.sensing.is_pro_spring:
            out += 'SRCD2N: '
            out += f'zpk([{fs1:.4f};{fs2:.4f}],[0.1;0.1],'
            out += f'{self.sensing.sensing_sign:.0f},"n")'
            out += f'gain({gainval:.2f})\n'
        else:
            out += f'SRCD2N: zpk([{Real:.4f}+i*{Imag:.4f};'
            out += f'{Real:.4f}-i*{Imag:.4f}],'
            out += f'[0.1;0.1],{self.sensing.sensing_sign:.0f},"n")'
            out += f'gain({gainval:.2f})\n'
        out += f'Gain: gain({1/MAP_values[0]:.4g})'

        return out

    def inverse_sensing_srcd2n_foton_filter_zpk(self, mcmc_chain, cftd=False):
        """
        Returns tuple of strings for each of z, p, k, and gain.

        Parameters
        ----------
        mcmc_chain : `float`, array-like
            The result from the run_mcmc() method

        cftd : boolean, optional
            if True then omit the 7000 Hz pole, nominally for the CFTD path

        """

        MAP_values = np.median(mcmc_chain, axis=0)

        if not self.sensing.is_pro_spring:
            # Take s^2/(s^2 + s0^2 - i*s*s0/Q) and solve denominator for zeros
            # fs for FOTON is abs(1/(2*pi*i)*s') where s' are the two solutions
            # to the quadratic formula - see alog LHO 31693
            fs1 = (1.0/(2.0*np.pi) *
                   (-2.0*np.pi*MAP_values[2]/MAP_values[3]/2.0 +
                    0.5*np.sqrt((2.0*np.pi*MAP_values[2]/MAP_values[3])**2 +
                                4.0*(2.0*np.pi*MAP_values[2])**2)))
            fs2 = (1.0/(2.0*np.pi) *
                   (-2.0*np.pi*MAP_values[2]/MAP_values[3]/2.0 -
                    0.5*np.sqrt((2.0*np.pi*MAP_values[2]/MAP_values[3])**2 +
                                4.0*(2.0*np.pi*MAP_values[2])**2)))
        else:
            # Take s^2/(s^2 - s0^2 + i*s*s0/Q) and solve denominator for zeros
            Real = MAP_values[2]/2.0/MAP_values[3]
            Imag = (MAP_values[2]/2.0/MAP_values[3] *
                    np.sqrt(4.0*MAP_values[3]**2-1))
            fs1 = Real + Imag*1j
            fs2 = Real - Imag*1j

        # Correct normalization
        # Make a ZPK filter that is the inverse of the single pole model
        # This means the cavity pole will become a zero
        # To keep the filter constrained, we include an artificial pole at
        # 7 kHz
        singlepolefilt = ZerosPolesGain(-2.0*np.pi*MAP_values[1],
                                        -2.0*np.pi*7000.0,
                                        7000.0/MAP_values[1])
        # We want the filter normalized at 500 Hz
        normalization_value_at_500Hz = \
            abs(freqresp(singlepolefilt, 2.0*np.pi*500.0)[1][0])
        # Now compute a ZPK filter that is the inverse of the optical response
        # by including the cavity pole and (anti-)spring. To keep the filter
        # constrained, we include two poles at 0.1 Hz and one pole at 7 kHz
        modelfilt = \
            ZerosPolesGain(
                -2.0*np.pi*np.array([MAP_values[1], fs1, fs2]),
                -2.0*np.pi*np.array([0.1, 0.1, 7000]),
                np.prod(-2.0*np.pi*np.array([0.1, 0.1, 7000.0])) /
                np.prod(-2.0*np.pi*np.array([MAP_values[1], fs1, fs2])))
        # The gain is the ratio of the single pole gain to the complete optical
        # response at 500 Hz
        gainval = normalization_value_at_500Hz / \
            abs(freqresp(modelfilt, 2.0*np.pi*500.0)[1][0])

        zeros_str = ''
        poles_str = ''
        k_str = ''
        gain_str = ''
        # Print output FOTON filter
        # out = 'Inverse Sensing FOTON values: '
        # out += '[NB: SRCD2N zpk gain based on sensing sign in parameters '
        # out += 'file]\n'
        if cftd is False:
            if not self.sensing.is_pro_spring:
                zeros_str += f'[{MAP_values[1]:.4f};'
                zeros_str += f'{fs1:.4f};{fs2:.4f}]'
                poles_str += '[0.1;0.1;7000]'
                k_str += f'{self.sensing.sensing_sign:.0f}'
                gain_str += f'{gainval:.2f}'
            else:
                zeros_str += f'[{MAP_values[1]:.4f};'
                zeros_str += f'{Real:.4f}+i*{Imag:.4f};{Real:.4f}-i*{Imag:.4f}]'
                poles_str += '[0.1;0.1;7000]'
                k_str += f'{self.sensing.sensing_sign:.0f}'
                gain_str += f'{gainval:.2f}'

        else:
            # Need to print a FOTON filter that has no cavity pole and no 7000 Hz
            # filter for the CFTD path
            # out += 'Inverse Sensing without cavity pole FOTON values '
            # out += 'for CFTD path: [NB: SRCD2N zpk gain based on sensing sign '
            # out += 'in parameters file]\n'
            if not self.sensing.is_pro_spring:
                zeros_str += f'[{fs1:.4f};{fs2:.4f}]'
                poles_str += '[0.1;0.1]'
                k_str += f'{self.sensing.sensing_sign:.0f}'
                gain_str += f'{gainval:.2f}'
            else:
                zeros_str += f'[{Real:.4f}+i*{Imag:.4f};'
                zeros_str += f'{Real:.4f}-i*{Imag:.4f}]'
                poles_str += '[0.1;0.1]'
                k_str += f'{self.sensing.sensing_sign:.0f}'
                gain_str += f'{gainval:.2f}'

        return (zeros_str, poles_str, k_str, gain_str)

    def stack_measurements(self, measurement_list, fmin=None, fmax=None,
                           fmin_list=None, fmax_list=None,
                           strict=False,
                           roaming_measurement_list_x=None,
                           roaming_measurement_list_y=None):
        """
        Stack measurements together where each measurement's model for known
        filtering and digital filters is removed and the time dependence is
        removed. This makes it appear as though the measurements are taken at
        the same time. Only unknown variations or low frequency sensing spring
        variations remain.

        This object and all objects in the measurement list need to have their
        maximum a postiori values saved to the JSON file because this method
        will query the JSON file provided in each `ProcessSensingMeasurement`
        object in the list

        Parameters
        ----------
        measurement_list : `ProcessSensingMeasurement` list
            a list of measurements to normalize
        fmin : `float`, optional
            minimum frequency used for the MCMC
        fmax : `float`, optional
            maximum frequency used for the MCMC
        fmin_list : `float` list, optional
            list of minimum frequencies used for the MCMC or None
        fmax_list : `float` list, optional
            list of maximum frequencies used for the MCMC or None
        strict : boolean, optional
            stack measurements strictly checking for matching MCMC executions
        roaming_measurement_list_x : tuple (model string, `Measurement`) list
            a list of measurements from the roaming lines analysis for x-arm
        roaming_measurement_list_y : tuple (model string, `Measurement`) list
            a list of measurements from the roaming lines analysis for y-arm

        Returns
        -------
        output : `list`, array-like
            list of stacked measurement frequencies, transfer functions,
            rescaled transfer functions (to reference), uncertainties, and
            residuals
        tdcfs : list
            list of time dependent correction factors for each measurement

        """
        assert ((fmin_list is None and fmax_list is None) or
                (len(measurement_list) == len(fmin_list) and
                 len(measurement_list) == len(fmax_list)) or
                (len(measurement_list) == len(fmin_list) and
                 fmax_list is None) or
                (len(measurement_list) == len(fmax_list) and
                 fmin_list is None))

        output = []
        tdcfs = []

        ref_date, ref_map, ref_spring = self.query_results_from_json(
            self.meas_type, fmin, fmax, strict=strict)
        ref_response_zpk = SensingModel.optical_response(
            ref_map[1], ref_map[2], ref_map[3], ref_spring)

        for idx, meas in enumerate(measurement_list):
            this_freq, this_resp, this_resp_unc = \
                meas.get_processed_measurement_response()
            if fmin_list is None and fmax_list is None:
                this_date, this_map, this_spring = meas.query_results_from_json(
                    self.meas_type, strict=strict)
            elif fmin_list is not None and fmax_list is None:
                this_date, this_map, this_spring = meas.query_results_from_json(
                    self.meas_type, fmin=fmin_list[idx], strict=strict)
            elif fmin_list is None and fmax_list is not None:
                this_date, this_map, this_spring = meas.query_results_from_json(
                    self.meas_type, fmax=fmax_list[idx], strict=strict)
            else:
                this_date, this_map, this_spring = meas.query_results_from_json(
                    self.meas_type, fmin_list[idx], fmax_list[idx],
                    strict=strict)

            # We want to compute the transfer function as though we were
            # measuring the detector at the same reference time, so we need
            # to divide out the optical response from this measurement **
            # and then multiply in the optical response from the reference
            # measurement.
            # ** Note that we divide out using the optical spring f_s and Q
            # from the reference and then multiply this back in. This is
            # because we'll let the GPR take care of covering any variations
            # due to a potentially poorly modeled optical spring
            this_response_zpk = SensingModel.optical_response(
                this_map[1], ref_map[2], ref_map[3], ref_spring)

            # Compute the transfer function response for the current
            # measurement model and the reference model
            this_model = this_map[0] * freqresp(
                this_response_zpk, 2.0*np.pi*this_freq)[1]
            ref_model = ref_map[0] * freqresp(
                ref_response_zpk, 2.0*np.pi*this_freq)[1]

            # The residual for this measurement is just the measured response
            # divided by the model for this measurement
            this_resid = this_resp / this_model

            # Now rescale this measurement by multiplying this measurement
            # residuals by the reference model. This is equivalent to dividing
            # out the model for this measurement and multiplying in the
            # reference model
            this_resp_r = ref_model * this_resid

            # Compute kappa_c as the ratio of the current measured gain to the
            # reference gain. We don't actually use this here other than as an
            # output
            kappa_c = this_map[0] / ref_map[0]

            output.append([this_freq, this_resp, this_resp_r, this_resp_unc, this_resid])
            tdcfs.append([kappa_c, this_map[1], ref_map[2], ref_map[3]])

        # Now go through the roaming line measurement list, which could be
        # the x or y arm Pcal
        roaming_measurement_dict = {'x': None, 'y': None}
        roaming_measurement_dict['x'] = roaming_measurement_list_x or []
        roaming_measurement_dict['y'] = roaming_measurement_list_y or []

        for arm in ['x', 'y']:
            for idx, meas in enumerate(roaming_measurement_dict[arm]):
                # for each measurement (txt file input) just grab the raw TF,
                # this is essentially DARM_ERR/PCAL = C
                this_freq, this_resp, coh, this_resp_unc = meas[1].get_raw_tf(
                    'PCAL', 'DARM_ERR')

                # PCAL is in the denominator (the "A channel"), so we divide the
                # raw TF by this transfer function
                # TODO: note that endstation is fixed to be True because the input
                #       data has been processed through an analysis that reads
                #       from the end station channel
                this_pcal_model = PcalModel(meas[0])
                pcal_correction = this_pcal_model.compute_pcal_correction(
                    this_freq, endstation=True, arm=arm.upper())
                this_resp /= pcal_correction

                # The residual sensing terms are divided out
                this_sensing_model = SensingModel(meas[0])
                C_res = this_sensing_model.sensing_residual(this_freq)
                this_resp /= C_res

                this_response_zpk = SensingModel.optical_response(
                    meas[1].fcc, this_sensing_model.detuned_spring_frequency,
                    this_sensing_model.detuned_spring_q,
                    this_sensing_model.is_pro_spring)

                # this_rep and this_rep_r are equivalent because all of the TDCF
                # values have been backed out of the measurement by the analysis
                # of data that was provided to us in the ASCII txt files
                # Compute the transfer function response for the current
                # measurement model and the reference model
                this_opt_gain = this_sensing_model.coupled_cavity_optical_gain \
                    * meas[1].kappa_c
                this_model = this_opt_gain * \
                    freqresp(this_response_zpk, 2.0*np.pi*this_freq)[1]

                # this_resp_r = this_resp
                this_resid = this_resp / this_model

                # Use the reference model to get the residuals
                ref_model = ref_map[0] * freqresp(
                    ref_response_zpk, 2.0*np.pi*this_freq)[1]

                this_resp_r = this_resid * ref_model
                kappa_c = this_opt_gain / ref_map[0]

                # Append to the output lists
                output.append([this_freq, this_resp, this_resp_r, this_resp_unc, this_resid])
                tdcfs.append([kappa_c, meas[1].fcc, ref_map[2], ref_map[3]])

        return output, tdcfs

    def run_gpr(self, frequencies, measurement_list, fmin=None, fmax=None,
                fmin_list=None, fmax_list=None,
                roaming_measurement_list_x=None,
                roaming_measurement_list_y=None,
                RBF_length_scale=1.0, RBF_length_scale_limits=(0.5, 1.5),
                gpr_flim=None, save_to_file=None, strict_stack=False):
        """
        Run a Gaussian Process Regression on a set of sensing function measurements

        Parameters
        ----------
        frequencies : `float`, array-like
            Frequencies at which to compute the GPR (Hz)
        measurement_list : `ProcessSensingMeasurement` list
            a list of measurements to normalize
        fmin : `float`, optional
            minimum frequency used for the MCMC of reference measurement
        fmax : `float`, optional
            maximum frequency used for the MCMC of reference measurement
        fmin_list : `float` list, optional
            list of minimum frequencies used for the MCMC or None
        fmax_list : `float` list, optional
            list of maximum frequencies used for the MCMC or None
        roaming_measurement_list_x : tuple (model string, `Measurement`) list
            a list of measurements from the roaming lines analysis for x-arm
        roaming_measurement_list_y : tuple (model string, `Measurement`) list
            a list of measurements from the roaming lines analysis for y-arm
        RBF_length_scale : `float`, optional
            Initial length scale guess for the RBF term of the GPR fit (in logarithmic frequency)
        RBF_length_scale_limits : pair of floats >= 0, optional
            The lower and upper bound on RBF_length_scale
        gpr_flim : `tuple`, optional
            Minimum and maximum frequency points to include in the GPR, (fmin, fmax)
        save_to_file : str, optional
            Filename (HDF5) to save the data from this result
        strict_stack : boolean, optional
            stack measurements strictly checking for matching MCMC executions

        Returns
        -------
        y_pred : `complex128`, array-like
            Best fit curve using the GPR and covariance kernel
        sigma : `float`, array-like
            Standard deviation for the GPR
        cov : `float`, array-like
            Covariance matrix for the GPR
        stacked_meas : `list`, array-like
            list of stacked measurement frequencies, transfer functions,
            rescaled transfer functions (to reference), uncertainties, and
            residuals
        tdcfs : list
            list of time dependent correction factors for each measurement

        """
        assert ((len(measurement_list) == len(fmin_list) and
                 len(measurement_list) == len(fmax_list)) or
                (len(measurement_list) == len(fmin_list) and
                 len(fmax_list) == 0) or
                (len(measurement_list) == len(fmax_list) and
                 len(fmin_list) == 0))

        y_pred, sigma, cov, stacked_meas, tdcfs, gpr = self._gpr(
            frequencies, measurement_list, fmin, fmax,
            fmin_list, fmax_list, RBF_length_scale,
            RBF_length_scale_limits, gpr_flim, strict_stack=strict_stack,
            roaming_measurement_list_x=roaming_measurement_list_x)

        print(f"Sensing GPR optimum: {gpr.kernel_}")

        if save_to_file is not None:
            save_gpr_to_hdf5(save_to_file, self.sensing, 'sensing', y_pred,
                             cov, frequencies)

        return y_pred, sigma, cov, stacked_meas, tdcfs, gpr


class ProcessActuationMeasurement(ProcessMeasurement):
    """
    This class is used in conjuction with measurement data and ouputs
    arrays used as input to MCMC and GPR routines.
    For reference, please see G1501518-v21 subway map, and specifically
    'MCMC input for A'.

    Parameters
    ----------
    config_file : `str`
        This is the *.ini model file to be used to process the measurement data
    meas_type : `str`
        This should be one of 'actuation_x_arm' or 'actuation_y_arm'
    meas_sus_exc_to_darm : `Measurement`
        This is the object that contains the data for the DARM_IN channel to
        suspension excitation response
    meas_pcal_to_darm : `Measurement`
        This is the object that contains data for the PCAL to DARM TF
    meas_tup_1 : `str`, tuple
        This should be ('channel A', 'channel B') for the first measurement
        Ex.: ('H1:SUS-ETMX_L3_CAL_EXC', 'H1:LSC-DARM1_IN1_DQ')
    meas_tup_2 : `str`, tuple
        This should be ('channel A', 'channel B') for the second measurement
        Ex.: ('H1:CAL-PCALY_RX_PD_OUT_DQ', 'H1:LSC-DARM_IN1_DQ')
    meas1_cohThresh : `float`, optional
        Coherence threshold that values in measurement 1 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    meas2_cohThresh : `float`, optional
        Coherence threshold that values in measurement 2 must be above to be
        included; valid values in the range [0,1]. (default = 0)
    json_results_file : `str`, optional
        Filename of a JSON file when stacking measurements or running GPR

    """

    def __init__(self, config_file, meas_type, meas_sus_exc_to_darm, meas_pcal_to_darm,
                 meas_tup_1, meas_tup_2, meas1_cohThresh=0, meas2_cohThresh=0,
                 json_results_file=None):
        if not (meas_type == 'actuation_x_arm' or
                meas_type == 'actuation_y_arm'):
            raise ValueError('Invalid meas_type')
        super().__init__(config_file, meas_sus_exc_to_darm, meas_pcal_to_darm,
                         meas_tup_1, meas_tup_2, meas1_cohThresh,
                         meas2_cohThresh, json_results_file)
        self.actuation = ActuationModel(config_file, measurement=meas_type)
        self.meas_type = meas_type

    def get_processed_measurement_response(self):
        """
        This method extracts the transfer function data using the channel names
        from the DTT files specified in the object and computes the measurement
        response by removing known parameters (see G1501518-v21).

        Returns
        -------
        frequencies : `float`, array-like
            frequency values of the transfer function, in units of Hz
        processed_measurement_response : `complex128`, array-like
            transfer function response of the actuation function, in units of
            newtons per driver output (amps or volts**2). For example, for TST
            the units will be in N/V**2
        processed_measurement_response_unc : `float`, array-like
            relative uncertainty of processed measurement data

        """

        # First get the intermediate data products from the measurement
        (frequencies, tf_meas1, tf_meas2, pcal_correction,
         processed_measurement_response_unc) = \
            self.pre_process_transfer_functions()

        # For the actuation function correction, we need the known terms
        correction_uim, correction_pum, correction_tst = \
            self.actuation.known_actuation_terms_for_measurement(frequencies)

        # Now bring everything together; see G1501518
        # Choose which transfer function based on the user input
        if 'L3' in self.meas_tup_1[0].split(':')[1]:
            processed_measurement_response = \
                (tf_meas1 / tf_meas2) * (pcal_correction / correction_tst)
        elif 'L2' in self.meas_tup_1[0].split(':')[1]:
            processed_measurement_response = \
                (tf_meas1 / tf_meas2) * (pcal_correction / correction_pum)
        elif 'L1' in self.meas_tup_1[0].split(':')[1]:
            processed_measurement_response = \
                (tf_meas1 / tf_meas2) * (pcal_correction / correction_uim)
        else:
            raise ValueError('Could not find L1, L2, or L3 in the',
                             'meas_tup_1 string')

        return (frequencies,
                processed_measurement_response,
                processed_measurement_response_unc)

    def rescale_actuation_by_tdcf_val(self, response, kappa_Ai=1.0, **kwargs):
        """
        This method rescales the response function by dividing out the kappa_Ai
        value

        Parameters
        ----------
        response : `complex128`, array-like
            Transfer function of the optical response, having divided out the
            known quantities from the measured transfer functions
        kappa_Ai : `float`, optional
            The time dependent correction factor for actuator gain for this
            measurement. The data is divided by this number, so if anything
            other than the default value is provided, the data will be scaled
            differently (default = 1)

        """

        return response / kappa_Ai

    def run_mcmc(self, fmin=None, fmax=None, priors_bound=None,
                 save_map_to_file=None, save_chain_to_file=None, **kwargs):
        """
        This method is what is used to process the actuation function
        measurement data

        Parameters
        ----------
        fmin : `float`, optional
            Optional minimum frequency value for the MCMC fitting. Default is
            the minimum frequency of xdata (default = None)
        fmax : `float`, optional
            Optional maximum frequency value for the MCMC fitting. Default is
            the maximum frequency of xdata (default = None)
        priors_bound: `float`, array-like, optional
            User-specified boundary of prior distribution. Default boundary
            is only for gain, gain must be larger or equal to 0.0.
            If choosing a different set of boundaries, then this argument
            should be in form of a 2D array, 2X2. First (second) element of
            each row corresponds to the lower (upper) bound of each
            parameters: gain, residual delay.
        save_map_to_file : `str`, optional
            Filename (JSON) to save the maximum a postiori values from this
            result
        save_chain_to_file : `str`, optional
            Filename (HDF5) to save the postirior chain from this result
        kwargs : optional
            other kwargs are passed to ProcessMeasurement._mcmc

        Returns
        -------
        chain : `float`, array-like
            The MCMC chain where index:
            - 0 is the gain in units of newtons per driver output (amps or
            volts**2). For example, for TST the units will be in N/V**2.
            - 1 is the residual time delay in units of seconds

        """
        global meas_type_gl
        meas_type_gl = self.meas_type

        (frequencies, processed_measurement_response,
         processed_measurement_response_unc) = \
            self.get_processed_measurement_response()

        # For the MCMC, we need to use the absolute error and not the relative
        # uncertainty
        processed_measurement_response_err = \
            processed_measurement_response_unc * \
            np.abs(processed_measurement_response)

        # crop data used in the MCMC
        xdata, ydata, yerr = self.crop_data(frequencies,
                                            processed_measurement_response,
                                            processed_measurement_response_err,
                                            fmin, fmax)

        # priors
        nwalkers = 1000
        if priors_bound is not None:
            mean_actuation_mag = (priors_bound[0][1] + priors_bound[0][0]) / 2
            actuation_sigma = (priors_bound[0][1] - priors_bound[0][0]) / np.sqrt(12)
            residual_delay_min = priors_bound[1][0]
            residual_delay_max = priors_bound[1][1]
        else:
            mean_actuation_mag = np.mean(np.abs(ydata))
            actuation_sigma = 0.3 * mean_actuation_mag
            residual_delay_min = -61e-6
            residual_delay_max = 61e-6
        priors = np.hstack((
            np.random.normal(mean_actuation_mag, actuation_sigma,
                             size=(nwalkers, 1)),
            np.random.uniform(
                residual_delay_min, residual_delay_max, size=(nwalkers, 1))))

        chain = self._mcmc(xdata, ydata, yerr, priors, priors_bound, **kwargs)

        if save_map_to_file is not None:
            self.save_results_to_json(
                save_map_to_file, fmin, fmax, np.median(chain, axis=0),
                self.meas_type)

        if save_chain_to_file is not None:
            save_chain_to_hdf5(
                save_chain_to_file, self.actuation.config_to_dict(), fmin, fmax,
                self.meas_type, chain)

        return chain

    def stack_measurements(self, measurement_list, fmin=None, fmax=None,
                           fmin_list=None, fmax_list=None, use_ini_reference=True,
                           strict=False, **kwargs):
        """
        Stack measurements together where each measurement's model for known
        filtering and digital filters is removed and the time dependence is
        removed. This makes it appear as though the measurements are taken at
        the same time. Only unknown variations or low frequency sensing spring
        variations remain.

        This object and all objects in the measurement list need to have their
        maximum a postiori values saved to the JSON file because this method
        will query the JSON file provided in each `ProcessSensingMeasurement`
        object in the list

        Additional kwargs parameters are unused but present in the definition
        of this method to serve as passthroughs. We need to clean this up.

        Parameters
        ----------
        measurement_list : `ProcessSensingMeasurement` list
            a list of measurements to normalize
        fmin : `float`, optional
            minimum frequency used for the MCMC
        fmax : `float`, optional
            maximum frequency used for the MCMC
        fmin_list : `float` list, optional
            list of minimum frequencies used for the MCMC or None
        fmax_list : `float` list, optional
            list of maximum frequencies used for the MCMC or None
        use_ini_reference : `boolean'
            flag to use the parameters for the reference model
            from the ini (default = True)

        Returns
        -------
        output : `list`, array-like
            list of stacked measurement frequencies, transfer functions,
            rescaled transfer functions (to reference), uncertainties, and
            residuals
        tdcfs : list
            list of time dependent correction factors for each measurement

        """
        assert ((len(measurement_list) == len(fmin_list) and
                 len(measurement_list) == len(fmax_list)) or
                (len(measurement_list) == len(fmin_list) and
                 len(fmax_list) == 0) or
                (len(measurement_list) == len(fmax_list) and
                 len(fmin_list) == 0))

        output = []
        tdcfs = []

        ref_map = self.query_results_from_json(self.meas_type, fmin, fmax,
                                               strict=strict)[1]

        for idx, meas in enumerate(measurement_list):
            this_freq, this_resp, this_resp_unc = \
                meas.get_processed_measurement_response()
            if fmin_list is None and fmax_list is None:
                this_map = meas.query_results_from_json(self.meas_type,
                                                        strict=strict)[1]
            elif fmin_list is not None and fmax_list is None:
                this_map = meas.query_results_from_json(
                    self.meas_type, fmin=fmin_list[idx], strict=strict)[1]
            elif fmin_list is None and fmax_list is not None:
                this_map = meas.query_results_from_json(
                    self.meas_type, fmax=fmax_list[idx], strict=strict)[1]
            else:
                this_map = meas.query_results_from_json(
                    self.meas_type, fmin_list[idx], fmax_list[idx],
                    strict=strict)[1]

            # We want to compute the transfer function as though we were
            # measuring the detector at the same reference time, so we need
            # to divide out the actuation response from this measurement **
            # and then multiply in the actuation response from the reference
            # measurement.
            # ** Note that we only scale by the gain and not any residual time
            # delay
            this_model = this_map[0]
            ref_model = ref_map[0]

            # The residual for this measurement is just the measured response
            # divided by the model for this measurement
            this_resid = this_resp / this_model

            # Now rescale this measurement by multiplying this measurement
            # residuals by the reference model. This is equivalent to dividing
            # out the model for this measurement and multiplying in the
            # reference model
            this_resp_r = ref_model * this_resid

            # Compute kappa_a as the ratio of the current measured gain to the
            # reference gain. We don't actually use this here other than as an
            # output
            kappa_a = this_map[0] / ref_map[0]

            output.append([this_freq, this_resp, this_resp_r, this_resp_unc, this_resid])
            tdcfs.append(kappa_a)

        return output, tdcfs

    def run_gpr(self, frequencies, measurement_list, fmin=None, fmax=None,
                fmin_list=None, fmax_list=None,
                RBF_length_scale=1.0, RBF_length_scale_limits=(0.5, 1.5),
                gpr_flim=None, save_to_file=None, strict_stack=False):
        """
        Run a Gaussian Process Regression on a set of actuation function measurements

        Parameters
        ----------
        frequencies : `float`, array-like
            Frequencies at which to compute the GPR (Hz)
        measurement_list : `ProcessSensingMeasurement` list
            a list of measurements to normalize
        fmin : `float`, optional
            minimum frequency used for the MCMC of reference measurement
        fmax : `float`, optional
            maximum frequency used for the MCMC of reference measurement
        fmin_list : `float` list, optional
            list of minimum frequencies used for the MCMC or None
        fmax_list : `float` list, optional
            list of maximum frequencies used for the MCMC or None
        RBF_length_scale : `float`, optional
            Initial length scale guess for the RBF term of the GPR fit (in logarithmic frequency)
        RBF_length_scale_limits : pair of floats >= 0, optional
            The lower and upper bound on RBF_length_scale
        gpr_flim : `tuple`, optional
            Minimum and maximum frequency points to include in the GPR, (fmin, fmax)
        save_to_file : str, optional
            Filename (HDF5) to save the data from this result
        strict_stack : boolean, optional
            stack measurements strictly checking for matching MCMC executions

        Returns
        -------
        y_pred : `complex128`, array-like
            Best fit curve using the GPR and covariance kernel
        sigma : `float`, array-like
            Standard deviation for the GPR
        cov : `float`, array-like
            Covariance matrix for the GPR
        stacked_meas : `list`, array-like
            list of stacked measurement frequencies, transfer functions,
            rescaled transfer functions (to reference), uncertainties, and
            residuals
        tdcfs : list
            list of time dependent correction factors for each measurement

        """
        assert ((len(measurement_list) == len(fmin_list) and
                 len(measurement_list) == len(fmax_list)) or
                (len(measurement_list) == len(fmin_list) and
                 len(fmax_list) == 0) or
                (len(measurement_list) == len(fmax_list) and
                 len(fmin_list) == 0))

        y_pred, sigma, cov, stacked_meas, tdcfs, gpr = self._gpr(
            frequencies, measurement_list, fmin, fmax,
            fmin_list, fmax_list, RBF_length_scale,
            RBF_length_scale_limits, gpr_flim, strict_stack=strict_stack)

        # save the result to HDF5
        if save_to_file is not None:
            save_gpr_to_hdf5(save_to_file, self.actuation, self.meas_type,
                             y_pred, cov, frequencies)

        return y_pred, sigma, cov, stacked_meas, tdcfs


def _ln_prob(pars, bound=None):
    """
    This is a helper function for the MCMC analysis and not intended for
    general use

    See https://emcee.readthedocs.io

    """

    if meas_type_gl == 'sensing':
        if include_spring_gl:
            if bound is None:
                if (pars[2] < 0.0 or pars[2] > 20.0 or pars[3] < 1e-2 or
                        pars[3] > 1.0):
                    return -np.inf
            else:
                if (pars[0] < bound[0][0] or pars[0] > bound[0][1] or
                        pars[1] < bound[1][0] or pars[1] > bound[1][1] or
                        pars[2] < bound[2][0] or pars[2] > bound[2][1] or
                        pars[3] < bound[3][0] or pars[3] > bound[3][1] or
                        pars[4] < bound[4][0] or pars[4] > bound[4][1]):
                    return -np.inf

            this_response = \
                pars[0] * freqresp(SensingModel.optical_response(
                    pars[1], pars[2], 1/pars[3], is_pro_spring_gl),
                    2.0*np.pi*xdata_gl)[1] * np.exp(-2.*np.pi*1j*pars[4] * xdata_gl)

        else:
            if bound is not None:
                if (pars[0] < bound[0][0] or pars[0] > bound[0][1] or
                        pars[1] < bound[1][0] or pars[1] > bound[1][1] or
                        pars[4] < bound[4][0] or pars[4] > bound[4][1]):
                    return -np.inf

            this_response = \
                pars[0] * freqresp(SensingModel.optical_response(
                    pars[1], 0, 1e-3, is_pro_spring_gl),
                    2.0*np.pi*xdata_gl)[1] * np.exp(-2.*np.pi*1j*pars[4] * xdata_gl)

    elif (meas_type_gl == 'actuation_x_arm'
          or meas_type_gl == 'actuation_y_arm'):
        if bound is None:
            if pars[0] <= 0.0:
                return -np.inf
        else:
            if (pars[0] < bound[0][0] or pars[0] > bound[0][1] or
                    pars[1] < bound[1][0] or pars[1] > bound[1][1]):
                return -np.inf
        this_response = (pars[0] *
                         np.exp(-2.*np.pi*1j*pars[1] * xdata_gl))
    return np.sum(_log_norm_pdf(ydata_gl, this_response, yerr_gl))


def _log_norm_pdf(x, mu, sigma):
    """
    This is a helper function for the MCMC and not intended for general use

    This calculates the log of a Whittle likelihood function for two dimensions,
    PDF(x|mu,sigma) = (2*pi*sigma**2) * exp[-(x-mu)**2/(2*sigma**2)], where the
    two dimensions originate from the real and imaginary contributions from the
    data. We assume that the uncertainty in the two dimensions is uncorrelated,
    and that sigma is the standard deviation for the Gaussian in each of the two
    dimensions. Here `x` are the data values, `mu` are the expected values,
    and `sigma` are the absolute error values (not relative error)

    """
    return -0.5*abs((x-mu)/sigma)**2 - np.log(2.0*np.pi*sigma**2)


def _isin(element, test_elements, rel_tol=1e-09, abs_tol=0.0):
    """
    This function is related to the numpy function isin, but here we allow
    for a user-specified tolerance based on math.isclose()
    Calculates element in test_elements, broadcasting over element only.
    Returns a boolean array of the same shape as element that is True where
    an element of element is in test_elements and False otherwise.

    We implement and use this function because apparently there are sometimes
    small numerical errors on the frequency values extracted from DTT files
    leading to errors when combining transfer functions from different
    measurements. It is not intended for general use.

    Parameters
    ----------
    element : `float`, array-like
        Input array
    test_elements : `float`, array-like
        The values against which to test each value of element
    rel_tol : float
        relative tolerance
    abs_tol : float
        minimum absolute tolerance - useful for comparisons near zero.
        abs_tol must be at least zero

    Returns
    -------
    isin : `boolean`, array-like
        Has the same shape as element. The values element[isin] are in
        test_elements

    """

    isin = np.empty(element.shape, dtype=bool)
    for i in range(len(element)):
        isin[i] = False
        for j in range(len(test_elements)):
            if math.isclose(element[i], test_elements[j], rel_tol=rel_tol,
                            abs_tol=abs_tol):
                isin[i] = True
                break

    return isin


class ProcessDACDrivenSensingElectronicsMeasurement(ProcessOneMeasurement):
    """
    Parameters
    ----------
    meas_obj_1 : `Measurement`
        This is the object that contains the data for DAC-Driven measurement electronics
        measurement
    meas_obj_2 : `Measurement`
        This is the object that contains the data for DAC-Driven measurement electronics
        measurement
    meas_tup_1 : `float`, optional
        This should be ('channel A', 'channel B') for the first measurement
        Ex.: ('H1:OMC-TEST_DCPD_EXC', 'H1:OMC-DCPD_A_OUT_DQ')
    meas_tup_2 : `float` list, optional
        This should be ('channel A', 'channel B') for the second measurement
        Ex.: ('H1:OMC-TEST_DCPD_EXC', 'H1:OMC-DCPD_A_OUT_DQ')
    meas1_cohThresh : `float` list, optional
        list of maximum frequencies used
    meas2_cohThresh : `float` list, optional
        list of maximum frequencies used

    Returns
    -------
    """

    def __init__(self, config_file, meas_obj, meas_tup, meas_cohThresh=0):
        super().__init__(config_file, meas_obj, meas_tup, meas_cohThresh)
        self.config = config_file
        self.sensing = SensingModel(config_file)
        self.actuation = ActuationModel(config_file, measurement='actuation_x_arm')
        self.elec_meas = Model(config_file, measurement='electronics-measurement')
        self.measurement = meas_obj
        self.meas_tup = meas_tup
        self.meas_cohThresh = meas_cohThresh

    def DACDrivenActuation(self, frequencies):
        """
        Compute actuation part of the DAC-drive measuement response

        Parameters
        ----------
        frequencies : `float`, array-like
            array of frequencies to compute DAC-driven measurement response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response

        """

        sus_to_iop_delay_response = dfreqresp(
            digital_delay_filter(1, 16384), 2.0*np.pi*frequencies/16384)[1]
        iop_to_analog_delay_response = dfreqresp(
            digital_delay_filter(4, 65536), 2.0*np.pi*frequencies/65536)[1]

        # digital anti-imaging filter
        digital_ai_filter_response = \
            self.actuation.digital_aa_or_ai_filter_response(frequencies)

        # analog anti-imaging filter response
        analog_ai_filter_response = \
            self.actuation.analog_aa_or_ai_filter_response(frequencies)

        # Unknown overall time delay
        unknown_actuation_delay = np.exp(-2.0*np.pi*1j *
                                         self.actuation.unknown_actuation_delay *
                                         frequencies)

        A_res = (sus_to_iop_delay_response *
                 iop_to_analog_delay_response *
                 digital_ai_filter_response *
                 analog_ai_filter_response *
                 unknown_actuation_delay)

        tf = self.elec_meas.dac_gain * A_res

        return tf

    def DACDrivenSensingElectronic(self, name, frequencies):
        """
        Compute the DAC-drive measuement response only sensing part as shown
        in Part IV of G2200551

        # TODO: current model disagrees with measurement. Need investigation.
        See LHO:63453

        Parameters
        ----------
        name : str
            a string (e.g., 'A' or 'A_A') indicating the OMC path name to be
            evaluated. This string should be listed in
            SensingModel.omc_path_names variable
        frequencies : `float`, array-like
            array of frequencies to compute DAC-driven measurement response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response
        """

        # Make sure that name is listed uniquely in self.omc_path_names
        assert len(set(self.sensing.omc_path_names)) == len(self.sensing.omc_path_names)

        response = \
            self.sensing.omc_path_response(name, frequencies)

        tf = response * self.elec_meas.ma_a * self.elec_meas.v2a

        return tf

    def fullDACDrivenMeasModel(self, name, frequencies):
        """
        Compute the full response of DAC-driven measurement model

        Parameters
        ----------
        name : str
            a string (e.g., 'A' or 'A_A') indicating the OMC path name to be
            evaluated. This string should be listed in
            SensingModel.omc_path_names variable
        frequencies : `float`, array-like
            array of frequencies to compute DAC-driven measurement response

        Returns
        -------
        tf : `complex128`, array-like
            transfer function response
        """

        A_DAC = self.DACDrivenActuation(frequencies)

        C_DAC = self.DACDrivenSensingElectronic(name, frequencies)

        tf = A_DAC * C_DAC

        return tf

    def get_processed_measurement_response(self):
        """
        Returns
        -------
        frequencies : `float` , array-like
            list of normalized measurements
        tf_meas1 : `complex128` , array-like
        tf_meas2 : `complex128` , array-like
        unc_meas1 : `float` , array-like
        unc_meas1 : `float` , array-like
        """

        # First get the intermediate data products from the measurement
        (frequencies, tf_meas, coh_meas, unc_meas) = \
            self.pre_process_transfer_functions()

        return frequencies, tf_meas, coh_meas, unc_meas

    @staticmethod
    def compare_dac_driven_meas_response(frequencies, tf_meas1, tf_meas2,
                                         show_tf_plot=None, show_compare_plot=None):
        """
        Parameters
        ----------
        frequencies : `float` , array-like
            frequency values of the transfer function, in units of Hz
        tf_meas1 : `complex128`, array-like
            the extracted transfer function from meas_tup_1, excluding
            frequency points below the meas1_cohThresh coherence threshold
        tf_meas2 : `complex128`, array-like
            the extracted transfer function from meas_tup_2, excluding
            frequency points below the meas2_cohThresh coherence threshold
        show_tf_plot : optional
            the plot for each transfer function
        show_compare_plot : optional
            the plot for two transfer function comparsion

        Returns
        -------
        mag_comp : `float` , array-like
            the ratio of magnitude between two measurements
        pha_comp : `float` , array-like
            the ratio of phase between two measurements
        """

        frequencies = frequencies[4:]
        tf_meas1 = tf_meas1[4:]
        tf_meas2 = tf_meas2[4:]

        mag_compare = np.abs(tf_meas2 / tf_meas1)
        pha_compare = np.angle(tf_meas2 / tf_meas1, deg=True)

        if show_tf_plot is not None:
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            ax1.semilogx(frequencies, np.abs(tf_meas1))
            ax1.semilogx(frequencies, np.abs(tf_meas2))
            ax1.set_title('H1 OMC DCPD Signal Chain TF')
            ax2 = fig.add_subplot(212)
            ax2.semilogx(frequencies, np.angle(tf_meas1, deg=True))
            ax2.semilogx(frequencies, np.angle(tf_meas2, deg=True))
            ax2.set_title('TIA S/N:S2100832 or SN02')

        if show_compare_plot is not None:
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            ax1.semilogx(frequencies, mag_compare)
            ax1.set_title('Signal Chain Ratio')
            ax2 = fig.add_subplot(212)
            ax2.semilogx(frequencies, pha_compare)
            ax2.set_title('WC S/N: S2101608')

        return mag_compare, pha_compare


class SingleRoamingLineMeasurement:
    def __init__(self, freq, mag, phase, coh, navg,
                 kappa_c, fcc, gps_start=None, gps_end=None,
                 unc_corr_file_path=None):
        """Class to enclose a single Roaming Line Measurement.

        Parameters
        ----------
        freq : float
            Measurement Frequency (Hz)
        mag : float
            Magnitude of measurement
        phase : float
            Phase of measurement (radians)
        coh : float
            Measurement coherence
        navg : int
            Number of averages used in measurement
        kappa_c : float
            kappa_c value associated with the measurement
        fcc : float
            fcc value associated with the measurement
        gps_start : float
            gps timestamp of the measurement start time
        gps_end : float
            gps timestamp of the measurement end time
        unc_corr_file_path : str
            path frequency dependent uncertainty file to include in uncertainty
            estimations. Nominally, this will be due to the elastic deformation
            or uncertainty in the placement of the pcal beams on the test
            masses.
        """
        self.freq = freq
        self.mag = mag
        self.phase = phase
        self.coh = coh
        self.navg = int(navg)
        self.kappa_c = kappa_c
        self.fcc = fcc
        self.unc_corr_file_path = unc_corr_file_path

        if gps_start is not None and gps_end is not None:
            self.integration_time = gps_end - gps_start
        else:
            self.integration_time = None
        self.gps_segment = (gps_start, gps_end)

    @property
    def averages(self):
        """Pass."""
        return self.navg

    @property
    def unc(self):
        coh = self.coh
        unc_raw_val = np.sqrt((1.0-coh+1e-6)/(2.0*(coh+1e-6)*self.averages))

        # include etm deformation correction for high frequencies
        # uncertainties must be summed in quadrature here
        unc_corr = self.hf_unc_correction()
        return np.sqrt(unc_raw_val**2 + unc_corr**2)

    def get_raw_tf(self, *args):
        '''Return raw transfer function measurement values.
        '''
        freq = np.array([self.freq])
        tf = np.array([self.mag * np.exp(1j * self.phase)])
        coh = np.array([self.coh])
        unc = np.array([self.unc])
        return freq, tf, coh, unc

    def hf_unc_correction(self):
        """Return uncertainty adjustment due to deformation of ETM.
        See T2300381 and G2302160.
        """
        if self.unc_corr_file_path is not None:
            fdata = np.loadtxt(self.unc_corr_file_path, delimiter=',')
            freqs = fdata[:, 0]
            uncs = fdata[:, 1]
            unc_corr = np.interp(self.freq, freqs, uncs)
        else:
            unc_corr = 0.0
        return unc_corr

    def __repr__(self):
        s = f"HighFreqMeas: {self.freq:0.2f}Hz, {self.gps_segment[0]}"
        return s

    def __str__(self):
        freq = self.freq
        tf_mag = self.mag
        tf_pha = self.phase
        coh = self.coh
        navg = self.navg
        kappa_c = self.kappa_c
        fcc = self.fcc
        seg_start = self.gps_segment[0]
        seg_end = self.gps_segment[1]
        dt_fmt = "%Y%m%dT%H%M%SZ"
        t_s = tconvert(seg_start, dt_fmt)
        t_e = tconvert(seg_end, dt_fmt)
        result = (f'{freq:0.4f}, {tf_mag:0.4f}, {tf_pha:0.4f}, '
                  f'{coh:0.4f}, {navg:d}, '
                  f'{kappa_c:0.4f}, {fcc:0.4f}, '
                  f'{int(seg_start)}, {int(seg_end)}, '
                  f'{t_s}, {t_e}')
        return result


class RoamingLineMeasurementFile:
    def __init__(self, meas_file, pcal_unc_corr_file=None):
        """Pass."""
        self.filename = meas_file
        self.data = np.loadtxt(meas_file, skiprows=1, usecols=range(9),
                               delimiter=',')
        if self.data.ndim == 1:
            self.data = np.reshape(self.data, (1, self.data.shape[0]))
        self.averages = None

        # take frequency from first row
        # this assumes all rows in file are for the same frequency
        self.frequency = self.data[0, 0]

        self.measurements = [SingleRoamingLineMeasurement(*vals,
                                                          pcal_unc_corr_file)
                             for vals in self.data]
        self.gps_segments = tuple(m.gps_segment for m in self.measurements)

    @property
    def latest_measurement(self):
        """Pass."""
        return self.measurements[-1]
