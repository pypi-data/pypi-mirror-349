import os
import glob
import shutil
import datetime

from gpstime import gpstime

from ._log import logger, CMDError
from ._const import (
    IFO,
    CAL_MEASUREMENT_ROOT,
    DEFAULT_CONFIG_PATH,
    PCAL_DELTAT_SECONDS_LIMIT,
)
from . import _util


def output_path_for_template(template, replacement, outdir=None):
    """return the measurement output path for a given template file

    The `replacement` string will replace the '_template_' string in
    the returned file name.

    If `outdir` is None, output paths will be in the default
    CAL_MEASUREMENT_ROOT location.

    """
    template_file = os.path.basename(template)
    template_base = template_file.split('__')[0]
    if outdir is None:
        outdir = os.path.join(
            CAL_MEASUREMENT_ROOT,
            template_base,
        )
    return os.path.join(
        outdir,
        template_file.replace('_template_', replacement)
    )


def find_measurements_from_template(template, extensions, search_dir=None):
    """find all measurement files corresponding to the specified template file

    If `outdir` is None, measurement files will found in the default
    paths in CAL_MEASUREMENT_ROOT.

    """
    # kind of a hack to use the same utility for generating
    # measurement output paths to create a glob for searching for
    # output measurement files.
    tlist = []
    for ext in extensions:
        tglob = output_path_for_template(template+ext, '*', outdir=search_dir)
        tlist.extend(glob.glob(tglob))

    return sorted(tlist)


def measurement_extract_datetime(mfile):
    """extract the datetime from a measurement file

    returns a datetime object

    """
    # FIXME: this heuristic is based on an assumed location and format
    # of the date in the file name, assumes date is ISO string after
    # final '_' separator.  this should be improved.
    ds = os.path.splitext(os.path.basename(mfile))[0].split('_')[-1]
    return _util.parse_timestamp(ds)


def find_closest_measurement(measurements, dt, strictly_before=False):
    """find the closest measurement to the specified datetime

    `measurements` should be a list of measurement files all
    corresponding to the same template.  For each measurement file,
    the datetime of the measurement is extracted from the filename and
    compared to the provided `dt` object.  The measurement closest to
    the provided `dt` is returned with the corresponding timedelta
    object.  If `strictly_before` is True, the closest measurement
    *before* the specified `dt` will be returned.

    """
    last = None
    for mfile in sorted(measurements, reverse=True):
        mdt = measurement_extract_datetime(mfile)
        diff = mdt - dt
        # if strictly before, break at first negative diff
        if strictly_before and diff <= datetime.timedelta(0):
            last = (mfile, diff)
            break
        # if new diff is smaller, keep going
        elif last is None or abs(diff) < abs(last[1]):
            last = (mfile, diff)
            continue
        # if new diff is bigger, the last one must have been smallest,
        # so break
        else:
            break
    return last


def check_pcal_deltat(deltat, name):
    """check that PCal measurement diff is within limits"""
    if deltat > datetime.timedelta(PCAL_DELTAT_SECONDS_LIMIT):
        raise CMDError(f"{name}/pcal measurement pair are not within {PCAL_DELTAT_SECONDS_LIMIT} seconds ({deltat} s)") # noqa E501


def find_measurement_set(config_file, search, skip_bb=False, no_bb_ok=False):
    """find loop/pcal measurement pairs

    `search` can either be a gpstime or datetime object, or a
    directory path.  If path is given, measurement files will be found
    in the specified path.  If a datetime string is given, measurement
    files occuring before the specified time will be found in the
    default CAL_MEASUREMENT_ROOT.

    Returns a nested dict for all Sensing and Actuation measurements,
    with the following leaf dict key/values:
      'loop': loop measurement file
      'pcal': pcal measurement file
      'deltat': datetime.timedelta between measurements

    The loop measurement will be either the one closest to the
    specified time (datetime) or the latest (path), and the pcal
    measurement will be the one closest to the loop measurement.

    Parameters
    ----------
    config_file : str
        Path to config file.
    search : str
        can either be a datetime string (GPS time acceptable, or
        'last'/'latest' keyword), or a directory path.  If path is given,
        measurement files will be found in the specified path.  If a
        datetime string is given, measurement files will be found in the
        default CAL_MEASUREMENT_ROOT.
    skip_bb : bool
        if False then look for and include the most recent pcal2darm broadband
        measurement in the mset
    no_bb_ok : bool
        if False and skip_bb is False then throw exception if no broadband
        measurment is found. If skip_bb is True then no_bb_ok is ignored.

    Returns
    -------
    measurement_files : dict
        nested dict for all Sensing and Actuation measurements,
        with the following leaf dict key/values:
          'loop': loop measurement file
          'pcal': pcal measurement file
          'deltat': datetime.timedelta between measurements

    """
    gt = None
    search_dir = None

    if isinstance(search, datetime.datetime):
        if not os.path.exists(CAL_MEASUREMENT_ROOT):
            raise CMDError(f"could not find CAL_MEASUREMENT_ROOT {CAL_MEASUREMENT_ROOT}.")
        gt = search
        logger.debug(f"searching for measurement set closest to {gt}...")

    elif isinstance(search, (str, os.PathLike)):
        if not os.path.exists(search):
            raise CMDError(f"unknown directory {search}")
        search_dir = search
        logger.debug(f"loading measurement set from directory {search_dir}...")

    else:
        stype = type(search)
        raise CMDError(f"unknown measurement set search type: '{search}' ({stype})")

    config = _util.load_config(config_file)

    logger.debug("finding PCal measurements...")
    pcal_files = find_measurements_from_template(
        os.path.splitext(config['PCal']['params']['template'])[0],
        config['Common']['allowed_meas_extensions'],
        search_dir=search_dir,
    )
    logger.debug(f'search dir: {search_dir}')
    if not pcal_files:
        raise CMDError("No PCal measurements found.")

    measurement_files = {}

    name = 'Sensing'
    logger.debug(f"finding {name} measurements...")
    sens_files = find_measurements_from_template(
        os.path.splitext(config['Sensing']['params']['template'])[0],
        config['Common']['allowed_meas_extensions'],
        search_dir=search_dir,
    )
    if not sens_files:
        raise CMDError(f"No {name} measurements found.")
    if gt:
        sens_closest, __ = find_closest_measurement(
            sens_files,
            gt,
            strictly_before=True,
        )
    else:
        sens_closest = sens_files[-1]
    logger.debug(f"finding closest PCal to {name}...")
    pcal_closest, deltat = find_closest_measurement(
        pcal_files,
        measurement_extract_datetime(sens_closest),
    )
    check_pcal_deltat(deltat, name)
    measurement_files[name] = {
        'loop': sens_closest,
        'pcal': pcal_closest,
        'deltat': deltat,
    }

    # find actuation measurements
    for stage, sdict in config['Actuation'].items():
        if stage == 'params':
            continue
        for optic, odict in sdict.items():
            if optic == 'params':
                continue
            name = f'Actuation/{stage}/{optic}'
            logger.debug(f"finding {name} measurements...")
            act_files = find_measurements_from_template(
                os.path.splitext(odict['params']['template'])[0],
                config['Common']['allowed_meas_extensions'],
                search_dir=search_dir,
            )
            if not act_files:
                continue
            if gt:
                act_closest, __ = find_closest_measurement(
                    act_files,
                    gt,
                    strictly_before=True,
                )
            else:
                act_closest = act_files[-1]
            logger.debug(f"finding closest PCal to {name}...")
            pcal_closest, deltat = find_closest_measurement(
                pcal_files,
                measurement_extract_datetime(act_closest),
            )
            check_pcal_deltat(deltat, name)
            measurement_files[name] = {
                'loop': act_closest,
                'pcal': pcal_closest,
                'deltat': deltat,
            }

    # find broadband measurements
    if not skip_bb:
        name = 'BroadBand'
        logger.debug(f'finding {name} measurements...')
        pcal_bb_files = find_measurements_from_template(
            os.path.splitext(config['BroadBand']['params']['template'])[0],
            config['Common']['allowed_meas_extensions'],
            search_dir=search_dir,
        )
        if not pcal_bb_files:
            if not no_bb_ok:
                raise CMDError(f"No {name} measurements found.")
            logger.debug('No broadband measurements found.')
        else:
            if gt:
                bb_closest, _ = find_closest_measurement(
                    pcal_bb_files,
                    gt,
                    strictly_before=True,
                )
            else:
                bb_closest = pcal_bb_files[-1]
            # FIXME: pcal2darm bb measurements should be considered "pcal" measurements.
            # but the mset system depends heavily on the 'loop'/'pcal'/'deltat' structure
            # for its logic (e.g. the mset __init__()) so I'm placing this meas. in
            # the loop value for now. We might reconsider how we handle non-pair
            # tf measurements
            measurement_files[name] = {
                'loop': None,
                'pcal': bb_closest,
                'deltat': None
            }

    return measurement_files


class MeasurementSet:
    """PyDARM Measurement Set class

    Holds information about a calibration measurement set.

    """

    def __init__(self, measurement_files):
        """initialize the measurement set

        Not intended to be initialized directly, see either the `find`
        or `import` class methods.

        `measurement_files` should be a dictionary of measurement
        files.

        """
        self.measurements = measurement_files
        # find the date of the latest measurement, to set as the
        # "valid_on" date
        last = gpstime.fromgps(0)
        for mset in self.measurements.values():
            try:
                mdt = measurement_extract_datetime(mset['loop'])
            except Exception:
                continue
            if mdt > last:
                last = mdt
        self.__valid_on = last
        self.__id = _util.gen_timestamp(self.valid_on)
        self.model_ini = None
        self.model = None

    @property
    def valid_on(self):
        """gpstime for the earliest known valid time of this measurement set"""
        return self.__valid_on

    @property
    def id(self):
        """measurement set ID is the timestamp of the valid_on date"""
        return self.__id

    def __repr__(self):
        """string represenation of MeasurementSet"""
        valid_on = self.valid_on
        return f'<MeasurementSet {self.id} (valid on "{valid_on}")>'

    def items(self):
        """iterate of measurements"""
        yield from self.measurements.items()

    def export(self, export_dir):
        """export a measurement set to a directory

        Copy all measurement files into the specified directory.

        """
        os.makedirs(export_dir, exist_ok=True)
        for mpair in self.measurements.values():
            for m in ['loop', 'pcal']:
                if mpair[m] is None:
                    # FIXME: we have to treat BB measurements a bit differently
                    # because they don't consist of a measurement pair; they're
                    # a single tf (e.g. pcal/deltal_external).
                    continue
                outpath = os.path.join(export_dir, os.path.basename(mpair[m]))
                # FIXME: should check that files are the same?
                #
                # NOTE: existing files should be "locked" (not
                # writable), so we can't overwrite them.
                if not os.path.exists(outpath):
                    shutil.copy(mpair[m], outpath)

        # copy high frequency measurements
        hfm_dn = 'hf_roaming_lines'
        hfm_dir = os.path.join(CAL_MEASUREMENT_ROOT, hfm_dn)
        if os.path.exists(hfm_dir):
            shutil.copytree(hfm_dir, os.path.join(export_dir, hfm_dn), dirs_exist_ok=True)
        else:
            logger.warning('WARNING: high frequency measurement directory not found'
                           f": {hfm_dir}")

    @classmethod
    def import_dir(cls, import_dir, config_file=None, **kwargs):
        """import measurement set from directory

        Essentially the inverse of the `export()` method.  Search the
        directory for measurement files corresponding to the template
        patterns specified in the config.

        If `config` is None, the specified directory will be searched
        for a config file.

        """
        if not config_file:
            config_file = os.path.join(import_dir, f'pydarm_cmd_{IFO}.yaml')
        measurement_files = find_measurement_set(config_file,
                                                 search=import_dir,
                                                 **kwargs)
        return cls(measurement_files)

    ##########

    @classmethod
    def find(cls, datetime_str='now', config_file=DEFAULT_CONFIG_PATH,
             **kwargs):
        """find the measurement set closest to the specified time

        Search CAL_MEASUREMENT_ROOT for sensing, actuation, and pcal
        measurements corresponding to the templates patterns specified
        in the config file that are closest to the specified time.
        `datetime_str` can be any date/time string accepted by the
        `gpstime` module (including GPS time stamps, and relatives
        dates like "yesterday", default is 'now').

        If `config_file` is not specified, the default config file
        path will be used (DEFAULT_CONFIG_PATH).

        """
        if datetime_str in ['last', 'latest']:
            datetime_str = 'now'
        gt = _util.parse_time(datetime_str)
        measurement_files = find_measurement_set(config_file, search=gt,
                                                 **kwargs)
        return cls(measurement_files)
