import numpy as np

import git
import json

from gpstime import gpstime
from foton import FilterFile

from ._log import logger, CMDError
from ._git import check_report_git_status
from ._const import (
    IFO,
    set_cal_data_root,
    CALCS_FILTER_FILE,
)
from ._report import Report
from . import _args
from . import _util
from ..utils import write_filter_module, write_dict_epics


def read_foton_filter_designs(report):
    """Read foton filter designs to be exported.

    Parameters
    ----------
    report : pydarm.cmd._report.Report

    """
    try:
        with open(report.gen_path('foton_filters_to_export.json'), 'r') as fin:
            filter_data = json.load(fin)
    except Exception as e:
        logger.error(f"Unable to read foton filter data: {e}")

    return filter_data


def read_epics_records_file(report):
    """Load EPICS Channel records to export."""
    dtype = np.dtype([('name', 'U64'), ('value', 'f')])
    er = np.loadtxt(report.gen_path("export_epics_records.txt"), dtype=dtype)
    return dict(er)


def add_args(parser):
    _args.add_report_argument(parser)
    parser.add_argument(
        '--push', action='store_true',
        help="push filters and TDCF EPICS records to front end"
    )


def main(args):
    """export parameters to front-end CALCS model

    This takes the parameters from the latest (or specified) report
    and writes them to the CALCS front end, either as EPICS records or
    foton filters.  This should be done only if the report to be
    exported has been properly reviewed.

    """
    try:
        report = Report.find(args.report)
    except FileNotFoundError as e:
        raise CMDError(e)
    logger.info(f"report found: {report.path}")

    # check that the report git repo is clean
    check_report_git_status(report, check_valid=True)

    report_int = report.id_int()
    hash_int = report.git_int()
    gds_hash_int = report.gds_file_hash()[1]

    ##########

    # set CAL_DATA_ROOT env var for core
    set_cal_data_root()

    # process Foton filters
    filter_data = read_foton_filter_designs(report)
    if args.push:
        logger.info(f"Exporting filters to {CALCS_FILTER_FILE}")
        foton_obj = FilterFile(CALCS_FILTER_FILE)

    for pname, pval in filter_data.items():
        logger.info(f"{pname}: {pval}")
        if args.push:
            write_filter_module(foton_obj, **pval)

    # process EPICS records
    logger.info("Processing EPICS records")
    epics_records = read_epics_records_file(report)
    write_dict_epics(epics_records, dry_run=(not args.push), IFO=IFO)

    # TODO: add ability to clear entries. this is done by setting Section.design = ''.

    # update the front end report status channels
    write_dict_epics(
        {
            'CAL-CALIB_REPORT_ID_INT': report_int,
            'CAL-CALIB_REPORT_HASH_INT': hash_int,
            'CAL-CALIB_REPORT_GDS_HASH_INT': gds_hash_int,
        },
        dry_run=(not args.push), IFO=IFO,
        as_float=False,
    )

    if args.push:
        # git tag the report as exported
        repo = git.Repo(report.path)
        gt = gpstime.parse("now")
        ts = _util.gen_timestamp(gt)
        tag = f"exported-{ts}"
        logger.info(f"git tagging report as exported: {tag}")
        repo.create_tag(
            tag,
            message=f"This report was exported on {gt}.",
        )

        logger.info(f"report exported: {report.id}")
        logger.info(f"{IFO}:CAL-CALIB_REPORT_ID_INT: {report_int}")
        logger.info(f"{IFO}:CAL-CALIB_REPORT_HASH_INT: {hash_int}")
        logger.info(f"{IFO}:CAL-CALIB_REPORT_GDS_HASH_INT: {gds_hash_int}")
