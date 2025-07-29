import logging

logger = logging.getLogger('pydarm')


def log_to_file(logger, path):
    """have logger additionally log to file

    """
    fh = logging.FileHandler(
        path,
        mode='a',
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            '%(asctime)s %(message)s'
        )
    )
    logger.addHandler(fh)


class CMDError(Exception):
    pass
