import argparse

from tabulate import tabulate

import epics
from foton import FilterFile

from ._log import logger
from ._const import IFO, CALCS_FILTER_FILE, STAGE_LABEL_MAP
from . import _args
from . import _util
from ..calcs import CALCSModel
from ..model import Model
from ..actuation import ActuationModel


def get_frontend_free_parameters(filter_file, spec_dict):
    """Read filter bank for free parameters

    """
    params = {}

    ff = FilterFile(filter_file)

    for param, fbanks in spec_dict.items():
        if param == 'Fcc':
            continue

        module = fbanks[0]['bank_name']
        index = fbanks[0]['mod_slot']

        index -= 1
        fsection = ff[module][index]
        fdesign = fsection.get_zpk(plane='n')
        gain = fdesign[-1] if not fsection.empty() else None
        params[param] = gain

    # Fcc is treated differently
    module = spec_dict['Fcc'][0]['bank_name']
    index = spec_dict['Fcc'][0]['mod_slot']
    fsection = ff[module][index-1]
    fdesign = fsection.get_zpk(plane='n')
    params['Fcc'] = fdesign[0][0] if not fsection.empty() else None

    return params


def fdelta(x, y):
    """calculate fractional difference"""
    # return abs(x-y)/abs(x)
    return ''


def add_args(parser):
    mgroup = parser.add_mutually_exclusive_group()
    _args.add_report_option(mgroup)
    _args.add_model_option(mgroup, default=None)
    parser.add_argument(
        '--foton-file', default=CALCS_FILTER_FILE,
        help=f"CALCS foton txt file (default: {CALCS_FILTER_FILE})")
    parser.add_argument(
        '--epics', action=argparse.BooleanOptionalAction, default=True,
        help="show EPICS record status")
    parser.add_argument(
        '--filters', action=argparse.BooleanOptionalAction, default=True,
        help="show foton filter status")


def main(args):
    """print model/pipeline status

    Inspect the state of the front end (CALCS) EPICS records and foton
    filter definitions, compare them against the values recommended by
    latest valid (or specified) report, and print the differences to
    the screen.

    """
    config = _util.load_config(args.config)

    model_file = _args.args_get_model(args)

    if args.filters:
        logger.info("checking filters...")

        logger.info(f"reading foton file {args.foton_file}...")
        ffp = get_frontend_free_parameters(
            args.foton_file,
            config['Common']['calcs_filters'],
        )

        mfp = {}

        # get sensing free params from model file
        model = Model(model_file)
        model_dict = model.config_to_dict()
        mfp['1/Hc'] = 1/float(model_dict['sensing']['coupled_cavity_optical_gain'])
        mfp['Fcc'] = float(model_dict['sensing']['coupled_cavity_pole_frequency'])

        # determine which actuation stages to get from cmd
        # get mapping 'EX/L1' -> 'uim_NpA'
        for k in _util.gen_config_calcs_filters_keys(config):
            stage, optic = k.split('/')
            arm_section = f'actuation_{optic[-1].lower()}_arm'

            act_model = ActuationModel(model_file, arm_section)

            stage_homonym = STAGE_LABEL_MAP[stage]['homonym']
            stage_unit_dpc = STAGE_LABEL_MAP[stage]['unit_drive_per_counts']
            stage_unit_nsc = STAGE_LABEL_MAP[stage]['unit_nospecial_char']
            mfp[k] = getattr(act_model,
                             f'{stage_homonym.lower()}_dc_gain_{stage_unit_dpc}')() \
                * getattr(act_model,
                          f'{stage_homonym}_{stage_unit_nsc}'.lower())

        table = []
        for param in ffp.keys():
            if param not in mfp.keys():
                continue
            mval = abs(mfp[param])
            fval = abs(ffp[param])
            delta = fdelta(mval, fval)
            table.append((param, mval, fval, delta))

        logger.info("model free parameters:\n")

        output = tabulate(
            table,
            headers=["parameter", "model value", "front-end value", "fractional delta"],
        )
        print(output)

        if args.epics:
            print()

    if args.epics:
        logger.info("checking EPICS records...")
        calcs = CALCSModel(model_file)
        table = []
        for record, mval in calcs.compute_epics_records(gds_pcal_endstation=False,
                                                        exact=True).items():
            channel = f"{IFO}:{record}"
            fval = epics.caget(channel)
            delta = fdelta(mval, fval)
            table.append((channel, mval, fval, delta))
        output = tabulate(
            table,
            headers=["EPICS record", "model value", "front-end value", "fractional delta"],
        )
        print(output)
