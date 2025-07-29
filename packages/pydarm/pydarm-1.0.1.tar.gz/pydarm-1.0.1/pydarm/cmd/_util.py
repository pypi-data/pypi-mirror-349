import os
import sys
import re
import datetime
import subprocess
from pathlib import Path

import yaml

from gpstime import gpstime

from .. import __version__
from ._log import logger


def mcmc_mode_check(x):
    x = str(x).lower()
    if x not in ['all', 'latest', 'none']:
        raise Exception("`mcmc_mode` must be one of: all, latest, none")
    return x


def load_config(config_file):
    """load configuration file for sensing and actuation function measurements

    Example actuation section this was written for:
    ```
    Actuation:
      params:
        # optic: 'ETMX'
        n_recent_meas: 0

      L1:
        params:
          mcmc_fmin: 11.0 # Hz
          mcmc_fmax: 90.0 # Hz

        EX:
          params:
            mcmc_fmin: 11.0 # Hz
            mcmc_fmax: 90.0 # Hz
          description: "actuation X L1 (UIM) stage response"
          template: "SUSETMX_L1_SS__template_.xml"
    ```

    Parameters
    ----------
    config_file : str
        Path to config file.

    Returns
    -------
    config : dict

    """
    logger.debug(f"config file: {config_file}")

    config_file = Path(config_file)

    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Default parameters in case something wasn't supplied
    defaults = {
        'n_recent_meas': 0,
        'meas_tags': [],
        'meas_dir': '',
        'out_dir': None,
        }

    # Define argument type processing beyond what yaml loading
    # already does
    argtypes = {
        'meas_dir': Path,
        'mcmc_mode': mcmc_mode_check
        }

    for key, val in defaults.items():
        if key not in config['Common'].keys():
            config['Common'][key] = val

    # Sensing and Actuation inherit from Common any params they
    # don't already have
    modes = ['Sensing', 'Actuation']
    for key, val in config['Common']['params'].items():
        for mode in modes:
            if key not in config[mode]['params'].keys():
                config[mode]['params'][key] = val

    # actuation stages inherit from Actuation any attributes they
    # don't already have
    stages = ['L1', 'L2', 'L3']
    optics = ['EX', 'EY', 'IX', 'IY']
    for key, val in config['Actuation']['params'].items():
        if key in stages:
            pass
        else:
            for stage in stages:
                if key not in config['Actuation'][stage]['params'].keys():
                    config['Actuation'][stage]['params'][key] = val

    # actuation optics inherit from stage any attributes they
    # don't already have
    for stage in stages:
        for optic in optics:
            if stage in config['Actuation'].keys() and \
               config['Actuation'][stage]:
                stageSection = config['Actuation'][stage]
                if optic in stageSection.keys() and stageSection[optic]:
                    opticSection = stageSection[optic]
                    if opticSection['params'] is None:
                        opticSection['params'] = stageSection['params']
                    else:
                        for key, val in stageSection['params'].items():
                            if key in opticSection['params'].keys():
                                pass
                            else:
                                opticSection['params'][key] = \
                                    stageSection['params'][key]

    # convert arguments to correct type
    for mode in ['Common', 'Actuation', 'Sensing']:
        for key in config[mode]['params'].keys():
            if key in argtypes.keys():
                config[mode]['params'][key] = argtypes[key](
                    config[mode]['params'][key])
    for stage in stages:
        if stage in config['Actuation'].keys() and config['Actuation'][stage]:
            stageSection = config['Actuation'][stage]
            if stageSection['params'] is not None:
                for key, val in stageSection['params'].items():
                    if key in argtypes.keys():
                        stageSection['params'][key] = argtypes[key](val)
                for optic in optics:
                    if optic in stageSection.keys() and stageSection[optic]:
                        opticSection = stageSection[optic]
                        if opticSection['params'] is None:
                            continue
                        for key2, val2 in opticSection['params'].items():
                            if key2 in argtypes.keys():
                                opticSection['params'][key2] = \
                                    argtypes[key2](val2)

    return config


# this is a "ISO 8601-1:2019, basic format" date/time format
DATETIME_FMT = '%Y%m%dT%H%M%SZ'


def gen_timestamp(dt=None):
    """generate an ISO-compatible timestamp string for a datetime object

    Used for measurement set and report IDs

    """
    if dt is None:
        dt = datetime.datetime.now(datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc).strftime(DATETIME_FMT)


def parse_timestamp(ds):
    """parse timestamp (generated with gen_timestamp) into a gpstime object

    """
    return gpstime.strptime(ds, DATETIME_FMT).replace(tzinfo=datetime.timezone.utc)


def parse_time(ds):
    """parse a date/time string into a gpstime object

    """
    try:
        return parse_timestamp(ds)
    except ValueError:
        return gpstime.parse(ds)


def edit_file(path, editor=None):
    """edit file with default editor

    """
    cmd = []
    if editor:
        cmd = editor.split()
    elif os.getenv('EDITOR'):
        cmd = os.getenv('EDITOR').split()
    else:
        # try to find XDG-specified handler for text/x-python
        from gi.repository import Gio
        mimetype = 'text/plain'
        # XDG DATA directories
        # http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
        xdg_share = [
            os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        ] + os.getenv('XDG_DATA_DIRS', '/usr/local/share:/usr/share').split(':')
        # get desktop handler for mimetype
        desktop = subprocess.check_output(
            ['xdg-mime', 'query', 'default', mimetype],
            universal_newlines=True,
        ).strip()
        # look for desktop file
        if desktop:
            for d in xdg_share:
                apath = os.path.join(d, 'applications', desktop)
                if not os.path.exists(apath):
                    continue
                # extract executable
                app = Gio.DesktopAppInfo.new_from_filename(apath)
                exe = app.get_executable()
                if exe:
                    cmd = [exe]
                    break
    if not cmd:
        cmd = ['emacs']
    cmd += [path]
    logger.debug(' '.join(cmd))
    try:
        try:
            subprocess.run(cmd)
        except OSError:
            sys.exit("Could not find editor: %s" % cmd[0])
    except KeyboardInterrupt:
        sys.exit()


def gen_config_calcs_filters_keys(config):
    calcs_keys = config['Common']['calcs_filters'].keys()
    pattern = re.compile(r"^L[1-3]/[E,I][X,Y]$")
    for key in filter(pattern.match, calcs_keys):
        yield key


def write_pydarm_version(path):
    """record the pydarm version to a file

    """
    with open(path, 'w') as f:
        f.write(f"{__version__}\n")


def write_report_version(report, path):
    """record a reports ID and git hash to a file

    Will produce a warning if the report has uncommitted changes.

    """
    ghash, dirty = report.git_status()
    if dirty:
        logger.warning(f"WARNING: report {report.id} has uncommitted changes!")
    with open(path, 'w') as f:
        f.write(f"{report.id} {report.git_status(as_str=True)}\n")


def hex2int(hexsha, digits=7):
    """convert hexidecimal digest into an integer.

    Take the first 'digits' of the hex and return an int.  The default
    'digits' is 7, which is a "standard" short git hex length that
    should be relatively unique, and is 28 bits, which fortunately
    fits into a standard EPICS 32-bit signed int.

    """
    return int(hexsha[:digits], 16)


def int2hex(intsha, digits=7):
    """convert integer into hex.

    The 'intsha' is converted to a hex string.  If hex is less than
    'digits' in length (default 7), the string is zero padded up to
    'digits'.

    """
    return hex(intsha)[2:].zfill(digits)
