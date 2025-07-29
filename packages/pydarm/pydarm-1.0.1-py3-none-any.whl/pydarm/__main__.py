# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Jameson Rollins (2021)
#               Evan Goetz (2021)
#
# This file is part of pyDARM.

import os
import sys
import signal
import logging
import argparse
from importlib import import_module

from . import __version__
from .cmd import CMDS
from .cmd._log import logger, CMDError
from .cmd._const import DEFAULT_CONFIG_PATH


# NOTE: we need to set the overall logger level to be the "lowest",
# but then we can adjust the stream handler level separately.
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())
handler.setFormatter(
    logging.Formatter('%(asctime)s %(message)s')
)
logger.addHandler(handler)


########################################


parser = argparse.ArgumentParser(
    prog='pydarm',
    description="""aLIGO calibration interface

""",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    '--version', '-v', action='version', version=__version__)
parser.add_argument(
    '--config', '-c', default=DEFAULT_CONFIG_PATH,
    help=f"pydarm cmd config YAML file ({DEFAULT_CONFIG_PATH})",
)
subparsers = parser.add_subparsers(
    metavar='COMMAND',
)


def add_subcommand(name):
    """helper function for adding subcommand to the parser from cmd modules

    The name provided should be the name of a module in the `cmd`
    sub-package.  Each module should include an `add_args` function
    for adding argparse arguments to the argparse parser, and a `main`
    function with the main subcommand logic.  The docstring of the
    main function will be the doc for the sub-command.

    """
    mod = import_module(f'.{name}', 'pydarm.cmd')
    func = mod.main
    sp = subparsers.add_parser(
        name,
        help=func.__doc__.splitlines()[0],
        description=func.__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sp.set_defaults(func=func)
    mod.add_args(sp)
    return sp


def main():
    for name in CMDS:
        add_subcommand(name)
    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        parser.exit()
    func = args.func
    del args.func
    logger.debug(args)
    func(args)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        main()
    except CMDError as e:
        sys.exit(f"ERROR: {e}")
