import os

import h5py
from matplotlib import pyplot as plt

from ._log import logger
from . import _args
from ._const import set_cal_data_root
from ..darm import DARMModel
from ..plot import BodePlot


DATA_SAVE_FORMATS = ['.hdf5', '.h5']


def add_args(parser):
    mgroup = parser.add_mutually_exclusive_group()
    _args.add_report_option(mgroup)
    _args.add_model_option(mgroup, default=None)
    _args.add_freqspec_option(parser)
    parser.add_argument(
        '--save', '-s', metavar='PATH', action='append',
        help=("save plot (.png/.pdf/.svg) or response data (.hdf5/.h5)"
              " (may be specified multiple times)"))


def main(args):
    """plot model frequency response

    """
    model_file = _args.args_get_model(args)

    freq = _args.freq_from_spec(args.freq)

    out_data_files = set()
    out_plot_files = set()
    if args.save:
        out_files = set(args.save)
        for path in out_files:
            if os.path.splitext(path)[1] in DATA_SAVE_FORMATS:
                out_data_files.add(path)
        out_plot_files = out_files - out_data_files

    ##########

    # set CAL_DATA_ROOT env var for core
    set_cal_data_root()

    # if args.model and os.path.splitext(args.model)[1] in DATA_SAVE_FORMATS:
    #     with h5py.File(args.model) as f:
    #         title = f.attrs.get('title', '')
    #         freq = f['Frequency'][:]
    #         G = f['Data']['DARM'][:]
    #         R = f['Data']['Response'][:]
    #         C = f['Data']['Sensing'][:]
    #         A = f['Data']['Actuation'][:]
    #         D = f['Data']['Digital'][:]

    # else:
    if True:
        DARM = DARMModel(model_file)
        title = f"{DARM.name} PyDARM model: {model_file}"
        G = DARM.compute_darm_olg(freq)
        R = DARM.compute_response_function(freq)
        C = DARM.sensing.compute_sensing(freq)
        A = DARM.actuation.compute_actuation(freq)
        D = DARM.digital.compute_response(freq)

    logger.info("generating bode plots...")
    bp = BodePlot(title=title)
    bp.plot(
        freq, G,
        label='DARM',
    )
    bp.plot(
        freq, C,
        label='Sensing',
        linestyle='--',
    )
    bp.plot(
        freq, A,
        label='Actuation',
        linestyle='--',
    )
    bp.plot(
        freq, D,
        label='Digital',
        linestyle='--',
    )
    bp.plot(
        freq, R,
        label='Response',
    )
    bp.legend()

    if args.save:
        for path in out_plot_files:
            logger.info(f'saving plot: {path}')
            bp.save(path)
        for path in out_data_files:
            logger.info(f'saving frequency response data: {path}')
            with h5py.File(path, 'w') as f:
                f.attrs['title'] = title
                f.create_dataset('Frequency', data=freq)
                g = f.create_group('Data')
                g.create_dataset('DARM', data=G)
                g.create_dataset('Sensing', data=C)
                g.create_dataset('Actuation', data=A)
                g.create_dataset('Digital', data=D)
                g.create_dataset('Response', data=R)
    else:
        plt.show()
