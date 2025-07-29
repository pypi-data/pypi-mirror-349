import os
import argparse

from ._log import CMDError
from ._const import (
    CAL_CONFIG_ROOT,
    CAL_TEMPLATE_ROOT,
    CAL_MEASUREMENT_ROOT,
    CAL_REPORT_ROOT,
)
from ._report import list_reports, Report


def iterate_dir(path, include_dir=False, reverse=False):
    """iterate over files in a directory

    filters out directories and files that end with '~'

    """
    if not os.path.exists(path):
        return
    for f in sorted(os.listdir(path), reverse=reverse):
        if not include_dir and os.path.isdir(os.path.join(path, f)):
            continue
        if f[-1] == '~':
            continue
        yield f


def print_path(root, name, prefix='', full=False, end='\n'):
    """print file name or path"""
    if full:
        path = os.path.join(root, name)
    else:
        path = name
    print(f'{prefix}{path}', end=end)


def print_report(report, list_files=False):
    print(f"IFO: {report.IFO}")
    print(f"report: {report.id}")
    print(f"report GPS: {report.id_int()}")
    print(f"date: {report.id_gpstime()}")
    git_str = report.git_status(as_str=True)
    print(f"git status: {git_str}")
    hash_int = report.git_int()
    print(f"git hash int: {hash_int}")
    if report.tags:
        tags = ' '.join(report.tags)
        print(f"tags: {tags}")
    else:
        print("tags: None")
    print(f"valid: {report.is_valid()}")
    print(f"exported: {report.was_exported()}")
    print(f"path: {report.path}")
    print(f"config file: {report.config_file}")
    print(f"model file: {report.model_file}")
    print(f"report file: {report.report_file}")
    print(f"GDS filter file: {report.gds_file}")
    print(f"GDS filter file hash: {report.gds_file_hash(as_str=True)}")
    print("measurement set:")
    for name, params in report.mset.items():
        print(f"  {name}:")
        for key, val in params.items():
            print(f"    {key}: {val}")
    if list_files:
        print("files:")
        for r, ds, fs in os.walk(report.path):
            if '.git' in ds:
                ds.remove('.git')
            print(f"  {r}/")
            for f in fs:
                path = os.path.join(r, f)
                print(f"  {path}")


def add_args(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--measurements', '-m', metavar='TYPE', nargs='?', default=argparse.SUPPRESS,
        help="list recent measurements, or all measurements of specific type")
    group.add_argument(
        '--report', '-r', metavar='REPORT_ID', nargs='?', default=argparse.SUPPRESS,
        help="list all reports in chronological order, or show single report contents if report ID specified (use 'last' for latest report)") # noqa E501
    parser.add_argument(
        '--full', '-f', action='store_true',
        help="list files with full path")


def main(args):
    """list config files, measurements, and reports

    """
    if hasattr(args, 'measurements'):
        if args.measurements is None:
            print(f"measurements: {CAL_MEASUREMENT_ROOT}")
            it = os.walk(CAL_MEASUREMENT_ROOT)
            it.__next__()
            for r, ds, fs in it:
                print_path(os.path.dirname(r), os.path.basename(r), prefix='  ', full=args.full)
                prefix = '    '
                for i, f in enumerate(sorted(fs, reverse=True)):
                    print_path(r, f, prefix=prefix, full=args.full)
                    if i > 5:
                        print(f'{prefix}...')
                        break
        else:
            root = os.path.join(CAL_MEASUREMENT_ROOT, args.measurements)
            print(f"measurements: {root}")
            if not os.path.exists(root):
                raise CMDError(f"unknown measurement type '{args.measurements}'.")
            for f in os.listdir(root):
                print_path(root, f, prefix="  ", full=args.full)

    elif hasattr(args, 'report'):
        if args.report is None:
            for report in list_reports(chronological=True, valid_only=False):
                base = os.path.basename(report.path)
                print_path(CAL_REPORT_ROOT, base, full=args.full, end='')
                tags = ' '.join(report.tags)
                if tags:
                    print(f" {tags}")
                else:
                    print()
        else:
            report = Report.find(args.report)
            print_report(report)

    else:
        print(f"config: {CAL_CONFIG_ROOT}")
        for f in iterate_dir(CAL_CONFIG_ROOT):
            print_path(CAL_CONFIG_ROOT, f, prefix='  ', full=args.full)

        print(f"templates: {CAL_TEMPLATE_ROOT}")
        for f in iterate_dir(CAL_TEMPLATE_ROOT):
            print_path(CAL_TEMPLATE_ROOT, f, prefix='  ', full=args.full)

        print(f"reports: {CAL_REPORT_ROOT}")
        for i, f in enumerate(iterate_dir(CAL_REPORT_ROOT, include_dir=True, reverse=True)):
            print_path(CAL_REPORT_ROOT, f, prefix='  ', full=args.full)
            if i > 5:
                print("  ...")
                break
