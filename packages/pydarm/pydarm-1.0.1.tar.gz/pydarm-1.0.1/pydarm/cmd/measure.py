import os
import argparse
import shutil
import time
import filecmp
import subprocess

import epics

from ._const import (
    IFO,
    CAL_CONFIG_ROOT,
    CAL_TEMPLATE_ROOT,
)
from . import _util
from ._log import logger, CMDError
from ._mset import output_path_for_template


def diag_run(run_xml, save_xml=None, dry=False):
    """execute a DTT measurement template

    """
    if not save_xml:
        save_xml = run_xml
    diag_cmd = f'''
open
restore {run_xml}
run -w
save {save_xml}
quit
'''
    print(diag_cmd)
    if not dry:
        subprocess.run(
            ['diag'],
            input=diag_cmd.strip(),
            text=True,
            check=True,
        )
        print()
        # FIXME: check for errors somehow


def touch(path):
    """touch a file"""
    open(path, 'w').close()

##################################################


def add_args(parser):
    parser.add_argument(
        'measurement', nargs='*',
        help="measurements to be run (by default user default sequence from config)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--dry-run', '--dry', action='store_const', dest='run', const='dry',
        help="dry run, show what would be done but don't actually run measurement")
    group.add_argument(
        '--run-interactive', action='store_const', dest='run', const='interactive',
        help="run measurement in interactive mode")
    group.add_argument(
        '--run-headless', action='store_const', dest='run', const='headless',
        help="run measurement in headless mode")
    group.add_argument(
        '--fake', action='store_const', dest='run', const='fake',
        help=argparse.SUPPRESS)


def main(args):
    """run calibration plant transer function measurements

    This command by default runs the full set of sensing and actuation
    chain calibration measurements.  The measurement config and
    templates are retrieved from the CAL_CONFIG_ROOT directory.  Each
    time a measurement is initiated a timestamped directory is created
    in the CAL_DATA_ROOT/measurements/ directory, and all resulting
    measurement output files are saved to that directory.

    When run without arguments the available measurements, the
    templates they use, and the default measurement sequence will be
    printed.

    A '--run-*' argument must be provided to actually run the
    measurements.

    """
    # https://cdswiki.ligo-wa.caltech.edu/wiki/TakingCalibrationMeasurements

    if not CAL_CONFIG_ROOT:
        raise CMDError("CAL_CONFIG_ROOT not defined.")

    logger.info(f"config file: {args.config}")

    config = _util.load_config(args.config)

    measurements = {}
    for nick, mref in config['Common']['measurements'].items():
        section = config
        for name in mref.split('/'):
            section = section[name]
        measurements[nick] = {
            'description': section['params']['description'],
            'template': os.path.join(
                CAL_TEMPLATE_ROOT,
                section['params']['template'],
            ),
        }

    logger.info("available measurements:")
    for meas, conf in measurements.items():
        print(f"  {meas:<4}: {conf['description']} ({conf['template']})")
        # check that all template files exist
        if not os.path.exists(conf['template']):
            raise CMDError(f"measurement '{meas}' template file not found: {conf['template']}")

    # construct the measurement sequence
    default_measurement_sequence = config['Common']['measurement_sequence']

    if not args.measurement:
        mseq = default_measurement_sequence
    else:
        mseq = args.measurement

    for meas in mseq:
        if meas not in measurements:
            raise CMDError(f"'{meas}' is not a valid measurement.")

    logger.info("measurement sequence:")
    logger.info(f"  {mseq}")

    if not args.run:
        logger.warning("Use --run-* option to actually execute measurement.")
        return

    ##################################################
    # pre measurement checks

    # checking guardian state
    if args.run:
        grd_info = config['Common']['required_grd_state']
        try:
            check_node, req_state = grd_info.split(':')
        except ValueError:
            logger.error("could not parse guardian state info from config:")
            logger.error(f"  Common/required_grd_state: {grd_info}")
            logger.error("should be '<NODE>:<STATE>'.")
            raise CMDError("could not check guardian state.")
        # check state
        if args.run in ['interactive', 'headless']:
            cur_state = epics.caget(f'{IFO}:GRD-{check_node}_STATE_S')
            if cur_state != req_state:
                msg = f"guardian node {check_node} is not in the correct state: {cur_state} != {req_state}" # noqa E501
                raise CMDError(msg)

    # FIXME: warning for thermalization status (less than an hour in
    # NLN)

    if args.run == 'interactive':
        print("""
Interactive CAL measurement interface

This will execute a series of closed loop measurements of the
interferometer using diaggui.  For each measurement, diaggui will be
opened with a temporary measurement template.  When diaggui opens,
click "Start" to start running the measurement.  Once the measurement
is complete, click File->Save to save the measurement, followed by
File-Exit to exit diaggui.  Make sure to not change any of the
measurement settings, and to always save the measurement data to the
same file when complete.
""")
        input("Press enter when you're ready to continue (or Ctrl-C to cancel): ")

    ##################################################
    # run measurements

    # loop over measurements
    for meas in mseq:
        logger.info("##########")

        measurement = measurements[meas]
        description = measurement['description']
        template_path = measurement['template']
        meas_timestamp = _util.gen_timestamp()

        output_path = output_path_for_template(template_path, meas_timestamp)

        logger.info(f"measurement: {meas}: {description} measurement")
        logger.info(f"measurement timestamp: {meas_timestamp}")
        logger.info(f"measurement template: {template_path}")
        logger.info(f"measurement output: {output_path}")

        if args.run in [None, 'dry']:
            continue

        else:
            logger.info(f"executing {args.run} {meas} measurement...")

            # FIXME: print expected measurement time
            # FIXME: progress bar?

            # interactive running
            if args.run == 'interactive':
                tmp_path = output_path + '.tmp'
                shutil.copy(template_path, tmp_path)
                logger.info(f"temporary measurement file: {tmp_path}")
                logger.warning("starting diaggui (this may take a minute)...")
                cmd = ['diaggui', tmp_path]
                logger.debug(cmd)
                logger.warning("hit 'Start' to start measurement, then 'Save' and 'Exit' when complete.") # noqa R501
                subprocess.run(
                    cmd,
                )
                logger.info(f"saving {meas} output...")
                os.rename(tmp_path, output_path)

            # headless run
            elif args.run == 'headless':
                diag_run(template_path, output_path, dry=not args.run)

            elif args.run == 'fake':
                logger.warning("FAKE")
                time.sleep(1)
                touch(output_path)

            # FIXME: somehow capture measurement errors

            if filecmp.cmp(template_path, output_path):
                raise CMDError("measurement error: output and template files are identical, was measurement actually run?  Aborting.") # noqa E501

            logger.info(f"{meas} measurement complete.")

        # FIXME: validate the output somehow

        # FIXME: capture IFO config (EPICS/foton/etc) at measurement time

        # FIXME: should we continue with the rest of the measurments
        # if there was an issue?

        if not os.path.exists(output_path):
            raise CMDError(f"output measurement file not found: {output_path}")
        logger.info(f"{meas} output: {output_path}")

        # remove write permission from the file, as an added measure
        # to make sure it's not modified
        os.chmod(output_path, 0o444)

    if args.run in [None, 'dry']:
        return

    logger.info("all measurements complete.")
