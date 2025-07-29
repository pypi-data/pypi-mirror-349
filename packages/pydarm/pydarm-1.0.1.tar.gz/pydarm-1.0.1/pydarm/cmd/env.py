from . import _const as const


def add_args(parser):
    pass


def main(args):
    """print environment and exit

    """
    print(f"IFO={const.IFO}")
    print(f"CAL_ROOT={const.CAL_ROOT}")
    print()
    print(f"CAL_CONFIG_ROOT={const.CAL_CONFIG_ROOT}")
    print(f"CAL_MEASUREMENT_ROOT={const.CAL_MEASUREMENT_ROOT}")
    print(f"CAL_REPORT_ROOT={const.CAL_REPORT_ROOT}")
    print(f"CAL_UNCERTAINTY_ROOT={const.CAL_UNCERTAINTY_ROOT}")
    print()
    print(f"CAL_DATA_ROOT={const.CAL_DATA_ROOT}")
    print(f"CHANSDIR={const.CHANSDIR}")
    print(f"CALCS_FILTER_FILE={const.CALCS_FILTER_FILE}")
