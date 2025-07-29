import os
import shutil
from pathlib import Path

from gpstime import gpstime
from datetime import timezone

from ._log import logger
from ._const import DEFAULT_UNCERTAINTY_CONFIG_FNAME
from ._util import write_report_version


class Uncertainty:
    def __init__(self, path):
        path = Path(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"path does not exist: {path}")
        self.__path = path
        try:
            with open(self.gen_path('gps')) as f:
                self.__gps = int(f.read().strip())
        except FileNotFoundError:
            epath = os.readlink(path)
            self.__gps = int(''.join(epath.split('/')))
        with open(os.path.join(self.path, 'report')) as f:
            data = f.read().strip()
            try:
                report, ghash = data.split()
            except ValueError:
                report = data
                ghash = '0000000'
        self.__report = report
        self.__ghash = ghash

    @property
    def path(self):
        """path to uncertainty directory"""
        return self.__path

    def gen_path(self, *args):
        """generate a path within the uncertainty directory"""
        return os.path.join(self.__path, *args)

    @property
    def gps(self):
        """uncertainty GPS"""
        return self.__gps

    @property
    def report(self):
        """report ID used to generate this uncertainty"""
        return self.__report

    @property
    def report_git_hash(self):
        """report git hash"""
        return self.__ghash

    def get_plot(self):
        try:
            return list(
                self.path.glob('calibration_uncertainty_*_compare.png')
            )[0]
        except IndexError:
            try:
                return list(
                    self.path.glob('calibration_uncertainty_*.png')
                )[0]
            except IndexError:
                return None

    def get_data_datetime(self):
        return gpstime.fromgps(int(self.gps))

    def get_gen_datetime(self):
        path = self.get_plot()
        return gpstime.fromtimestamp(
            os.path.getmtime(path)
        ).astimezone(timezone.utc).replace(microsecond=0)

    @classmethod
    def create(cls, gps, report, uncertainty_config, path):
        """create an uncertainty directory

        """
        assert isinstance(gps, int), "Uncertainty GPS time must be an int"
        # logger.debug(f"uncertainty GPS: {report.id}")
        # logger.debug(f"uncertainty path: {path}")
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'gps'), 'w') as f:
            f.write(f"{gps}\n")
        write_report_version(report, os.path.join(path, 'report'))
        try:
            shutil.copy(
                uncertainty_config,
                os.path.join(path, DEFAULT_UNCERTAINTY_CONFIG_FNAME),
            )
        except shutil.SameFileError:
            logger.debug("Skipped copy: same file")
        return cls(path)
