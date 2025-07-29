import os


# instrument designator
IFO = os.getenv('IFO')
SITE = None
if IFO:
    IFO = IFO.upper()
if not IFO:
    pass
elif IFO == 'H1':
    SITE = 'LHO'
elif IFO == 'L1':
    SITE = 'LLO'
else:
    raise ValueError(f"unknown IFO '{IFO}'")


CAL_ROOT = None
if IFO:
    CAL_ROOT = os.path.join(
        '/ligo/groups/cal/',
        IFO,
    )
CAL_ROOT = os.getenv(
    'CAL_ROOT',
    CAL_ROOT,
)
if not CAL_ROOT:
    raise ValueError("CAL_ROOT not specified.")


CAL_CONFIG_ROOT = os.getenv(
    'CAL_CONFIG_ROOT',
    os.path.join(CAL_ROOT, 'ifo'),
)
CAL_DATA_ROOT = os.getenv(
    'CAL_DATA_ROOT',
    os.path.join(CAL_ROOT, 'data'),
)
CAL_MEASUREMENT_ROOT = os.getenv(
    'CAL_MEASUREMENT_ROOT',
    os.path.join(CAL_ROOT, 'measurements'),
)
CAL_REPORT_ROOT = os.getenv(
    'CAL_REPORT_ROOT',
    os.path.join(CAL_ROOT, 'reports'),
)
CAL_UNCERTAINTY_ROOT = os.getenv(
    'CAL_UNCERTAINTY_ROOT',
    os.path.join(CAL_ROOT, 'uncertainty'),
)


def set_cal_data_root():
    # the only way to communicate CAL_DATA_ROOT to the core library is
    # via the environment.  we make sure it's set here, so that it's
    # always set properly for the report generation below.  a default
    # value will be used if the it wasn't set in the environment (see
    # _const)
    os.environ['CAL_DATA_ROOT'] = CAL_DATA_ROOT
    return CAL_DATA_ROOT


CAL_TEMPLATE_ROOT = os.path.join(CAL_CONFIG_ROOT, 'templates')
DEFAULT_MODEL_PATH = None
DEFAULT_MODEL_FNAME = None
DEFAULT_CONFIG_PATH = None
DEFAULT_CONFIG_FNAME = None
DEFAULT_UNCERTAINTY_CONFIG_PATH = None
DEFAULT_UNCERTAINTY_CONFIG_FNAME = None
if IFO:
    DEFAULT_MODEL_FNAME = f'pydarm_{IFO}.ini'
    DEFAULT_CONFIG_FNAME = f'pydarm_cmd_{IFO}.yaml'
    DEFAULT_UNCERTAINTY_CONFIG_FNAME = f'pydarm_uncertainty_{IFO}.ini'

    DEFAULT_MODEL_PATH = os.path.join(
        CAL_CONFIG_ROOT,
        DEFAULT_MODEL_FNAME,
    )
    DEFAULT_CONFIG_PATH = os.path.join(
        CAL_CONFIG_ROOT,
        DEFAULT_CONFIG_FNAME,
    )
    DEFAULT_UNCERTAINTY_CONFIG_PATH = os.path.join(
        CAL_CONFIG_ROOT,
        DEFAULT_UNCERTAINTY_CONFIG_FNAME,
    )


CHANSDIR = None
if IFO:
    CHANSDIR = os.path.join(
        '/opt/rtcds',
        SITE.lower(),
        IFO.lower(),
        'chans'
    )
CHANSDIR = os.getenv(
    'CHANSDIR',
    CHANSDIR,
)

CALCS_FILTER_FILE = None
if CHANSDIR:
    CALCS_FILTER_FILE = os.path.join(
        CHANSDIR,
        f'{IFO}CALCS.txt',
    )


# default frequency response frequency array
DEFAULT_FREQSPEC = '0.01:5000:3000'


# maximum allowable time difference measurement and corresponding PCal
# measurement
PCAL_DELTAT_SECONDS_LIMIT = 20*60


# free parameter plot labels
FREE_PARAM_LABEL_MAP = {
    'Hc': {
        'label': 'Optical gain, H_c (ct/m)',
        'mathlabel': r'$H_C$',
    },
    '1/Hc': {
        'label': 'Inv. Optical gain, H_c (m/ct)',
        'mathlabel': r'$H_C^{-1}$',
    },
    'Fcc': {
        'label': 'Cavity_pole, f_cc (Hz)',
        'mathlabel': r'$f_{cc}$',
    },
    'Fs': {
        'label': 'Detuned SRC spring frequency, f_s (Hz)',
        'mathlabel': r'$f_s$',
    },
    'Qs': {
        'label': 'Detuned SRC spring quality factor, Q_s',
        'mathlabel': r'$Q$',
    },
    'tau_C': {
        'label': 'Residual time delay, tau_c (s)',
        'mathlabel': r'$\Delta\tau_C$',
    },
    # actuation parameters
    'L1': {
        'label': 'Actuation Gain, Hau (N/A)',
        'mathlabel': '$H_{UIM}$',
        'textlabel': 'Hau',
    },
    'L2': {
        'label': 'Actuation Gain, Hap (N/A)',
        'mathlabel': '$H_{PUM}$',
        'textlabel': 'Hap'
    },
    'L3': {
        'label': 'Actuation Gain, Hat (N/V**2)',
        'mathlabel': '$H_{TST}$',
        'textlabel': 'Hat'
    },
    'tau_A': {
        'label': 'Residual time delay, tau_A (s)',
        'mathlabel': '$\\Delta\\tau_A$'
    }
}


# labels and units for the actuation stages
STAGE_LABEL_MAP = {
    'L1': {'homonym': 'UIM',
           'unit': 'N/A',
           'unit_nospecial_char': 'NpA',
           'unit_drive_per_counts': 'Apct'
           },
    'L2': {'homonym': 'PUM',
           'unit': 'N/A',
           'unit_nospecial_char': 'NpA',
           'unit_drive_per_counts': 'Apct'
           },
    'L3': {'homonym': 'TST',
           'unit': 'N/V**2',
           'unit_nospecial_char': 'NpV2',
           'unit_drive_per_counts': 'V2pct'
           }
}
