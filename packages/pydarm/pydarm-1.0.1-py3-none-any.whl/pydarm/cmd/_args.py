import os
import argparse

import numpy as np

from ._log import logger, CMDError
from ._const import (
    DEFAULT_MODEL_PATH,
    DEFAULT_FREQSPEC,
    IFO
)
from ._report import Report


class ModelNameParseAction(argparse.Action):
    """model path argparse argument parser Action.

    """
    help = 'model INI config file'

    def __init__(self, *args, **kwargs):
        kwargs['metavar'] = kwargs.get('metavar', 'MODEL')
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=False):
        if not values:
            raise argparse.ArgumentError(self, f"the following argument is required: {self.metavar}") # noqa E501
        path = values
        if not os.path.exists(path):
            raise argparse.ArgumentError(self, f"model file not found: {path}")
        setattr(namespace, self.dest, path)


def add_model_option(parser, default=DEFAULT_MODEL_PATH, **kwargs):
    """add a subparser argument for a model file"""
    help = "model parameter INI file"
    if default:
        help += f" ({default})"
    parser.add_argument(
        '--model', '-m', action=ModelNameParseAction, default=default,
        help=help,
        **kwargs
    )


def add_report_argument(parser):
    """add a subparser argument for a report ID"""
    parser.add_argument(
        'report', metavar='REPORT_ID', default='last', nargs='?',
        help="report ID to process, or 'last' for latest report (default)"
    )


def add_report_option(parser, default='last', **kwargs):
    """add a subparser option for a report ID"""
    help = "report ID to process, or 'last' for latest report"
    if default:
        help += f" ({default})"
    parser.add_argument(
        '--report', '-r', metavar='REPORT_ID', default=default,
        help=help,
        **kwargs
    )


def args_get_model(args):
    """get the model file from report or model spec

    """
    if getattr(args, 'model'):
        model_file = args.model
        logger.info(f"using specified model file: {model_file}")
    else:
        logger.info(f"searching for '{args.report}' report...")
        report = Report.find(args.report)
        logger.info(f"found report: {report.id}")
        # model_file = report.model_file
        model_file = report.gen_path(f'pydarm_{IFO}.ini')
        logger.info(f"using model from report: {model_file}")
    if not os.path.exists(model_file):
        raise CMDError("model file not found.")
    return model_file


def freq_from_spec(spec):
    """logarithmicly spaced frequency array, based on specification string

    Specification string should be of form 'START:[NPOINTS:]STOP'.

    """
    fspec = spec.split(':')
    if len(fspec) == 2:
        fspec = fspec[0], DEFAULT_FREQSPEC.split(':')[1], fspec[1]
    return np.geomspace(
        float(fspec[0]),
        float(fspec[2]),
        num=int(fspec[1]),
    )


def add_freqspec_option(parser, default=DEFAULT_FREQSPEC, **kwargs):
    """add a subparser option for specifying a frequency array"""
    parser.add_argument(
        '--freq', '-f', metavar='FLO:[NPOINTS:]FHI', default=default,
        help=f'logarithmic frequency array specification in Hz [{default}]',
        **kwargs
    )
