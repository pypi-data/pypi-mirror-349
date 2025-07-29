import os
import re
import glob
import json
import shutil
import hashlib
from pathlib import Path
from subprocess import run

import git

import gpstime

from ._log import logger
from ._const import (
    IFO,
    CAL_REPORT_ROOT,
    DEFAULT_CONFIG_FNAME,
    DEFAULT_MODEL_FNAME,
)
from . import _util
from ._mset import MeasurementSet
from ..darm import DARMModel
from ..calcs import CALCSModel
from ..measurement import (
    Measurement,
    ProcessSensingMeasurement,
    ProcessActuationMeasurement,
)


MODEL_INI_RE = re.compile("pydarm_(?P<IFO>..).ini")


def git_global_config_set_safe_directory(path):
    """globally configure git to set path as safe directory"""
    try:
        paths = run(
            ['git', 'config', '--global', '--get-all', 'safe.directory'],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    except Exception:
        # if this call fails then I just note it and hope for the
        # best.  The usual case where this would fail is on the
        # ldas-jobs web servers
        return
    if set(('*', str(path))).isdisjoint(paths):
        logger.warning("NOTE: Adding safe.directory exception for report path to user global git config.")  # noqa E501
        logger.warning("This is needed to allow access to shared git repos.")
        logger.warning("To subvert future warnings, consider adding a blanket safe.directory exception:")  # noqa E501
        logger.warning("    git config --global --add safe.directory '*'")
        run(
            ['git', 'config', '--global', '--add',
             'safe.directory', path],
            check=True,
        )


class Report:
    """Report class

    This class holds information about a calibration report.

    """

    def __init__(self, path):
        """initialize Report object from a report directory

        """
        # this will strip of trailing slashes
        path = Path(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"path does not exist: {path}")

        # because the report directories are shared we need to make
        # exceptions for them in the users config
        # FIXME: we should definitely not be mucking with the users global
        # config settings, but i'm not sure how else to get around this
        # FIXME: should we do this globally with '*'? that seems extreme
        git_global_config_set_safe_directory(path)

        self.__path = path
        try:
            with open(self.gen_path('id')) as f:
                self.__id = f.read().strip()
        except FileNotFoundError:
            self.__id = os.path.basename(path)
        ini_matches = []
        for f in glob.iglob(self.gen_path("pydarm_*.ini")):
            ini_match = MODEL_INI_RE.match(os.path.basename(f))
            if ini_match:
                ini_matches.append(ini_match)
        if len(ini_matches) == 0:
            raise RuntimeError(f"directory {self.__path} does not include a model ini file")
        elif len(ini_matches) > 1:
            raise RuntimeError(f"directory {self.__path} includes multiple model ini files, can not determine IFO")  # noqa E501
        self.__model_file = self.gen_path(ini_matches[0].string)
        self.__IFO = ini_matches[0].group('IFO')
        if self.__IFO != IFO:
            logger.warning(f"WARNING: current IFO is {IFO}, but report {self.__id} corresponds to IFO '{self.__IFO}'")  # noqa E501
        ghash, dirty = self.git_status()
        if dirty:
            logger.debug(f"WARNING: report has a dirty working tree! :: {self.__id} ")
        self.__calcs = None
        self.__config = None
        self.__mset = None
        self.measurements = None

    @property
    def path(self):
        """path to report directory"""
        return self.__path

    def gen_path(self, *args):
        """generate a path within the report directory"""
        return os.path.join(self.__path, *args)

    @property
    def id(self):
        """report ID"""
        return self.__id

    def __eq__(self, other):
        """equal if report IDs match"""
        # FIXME: are there other things we should be checking here?
        return self.id == other.id

    def id_gpstime(self):
        """parse report ID into gpstime object"""
        return _util.parse_timestamp(self.id)

    def gps(self):
        """GPS time of report"""
        return self.id_gpstime().gps()

    def id_int(self):
        """report ID as an GPS time int (used for EPICS encoding)"""
        return int(self.gps())

    @property
    def IFO(self):
        """IFO for which this report is associated"""
        return self.__IFO

    ##########

    def git_status(self, as_str=False):
        """git status of report

        Return tuple of the git hash and a bool that indicates is True
        if the working tree is dirty.

        """
        try:
            repo = git.Repo(self.path)
            ghash = repo.head.commit.hexsha
            dirty = repo.is_dirty()
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            ghash = '00000000'
            dirty = True
        if as_str:
            git_str = ghash[:7]
            if dirty:
                git_str += '*'
            return git_str
        else:
            return ghash, dirty

    def git_int(self):
        """git commit hash as an int"""
        ghash, dirty = self.git_status()
        return _util.hex2int(ghash)

    def _git_tags(self):
        """git tags on the current head"""
        try:
            return git.Repo(self.path).git.tag(points_at='HEAD').splitlines()
        except git.exc.InvalidGitRepositoryError:
            return []

    ##########

    def __repr__(self):
        """string representation of Report"""
        git_str = self.git_status(as_str=True)
        return f'<Cal Report {self.IFO} {self.id} {self.path} {git_str}>'

    @property
    def model_file(self):
        """path to report model INI file"""
        return self.__model_file

    @property
    def model(self):
        """DARMModel"""
        return DARMModel(self.model_file)

    @property
    def calcs(self):
        """CALCSModel"""
        return CALCSModel(self.model_file)

    @property
    def pcal(self):
        """PcalModel"""
        return self.model.pcal

    @property
    def config_file(self):
        """path to report cmd config file"""
        return self.gen_path(
            f'pydarm_cmd_{self.IFO}.yaml'
        )

    @property
    def config(self):
        """parsed config parameters"""
        if self.__config is None:
            self.__config = _util.load_config(self.config_file)
        return self.__config

    @property
    def report_file(self):
        """path to model report PDF file"""
        return self.gen_path(
            f"{self.IFO}_calibration_report_{self.id}.pdf",
        )

    @property
    def gds_file(self):
        """path to GDS filter file"""
        return self.gen_path(f'gstlal_compute_strain_C00_filters_{self.IFO}.npz')

    def gds_file_hash(self, as_str=False):
        """sha256 hash of GDS filter file

        returns a tuple of the hash and an int encoding of the hash,
        or a string representation if as_str=True.

        """
        with open(self.gds_file, 'rb') as f:
            fhash = hashlib.sha256(f.read()).hexdigest()
        fhash_int = _util.hex2int(fhash)
        if as_str:
            return f'{fhash} [{fhash_int}]'
        else:
            return fhash, fhash_int

    def gen_mpath(self, *args):
        """generate a path in the measurement sub-directory

        """
        # FIXME: this is to support both new (measurement subdir) and
        # old style reports, could fully deprecate old style at some
        # point
        if os.path.exists(self.gen_path('measurements')):
            return self.gen_path('measurements', *args)
        else:
            return self.gen_path(*args)

    @property
    def mset(self):
        """return the MeasurementSet for this report"""
        if self.__mset is None:
            self.__mset = MeasurementSet.import_dir(
                self.gen_mpath(),
                config_file=self.config_file,
                no_bb_ok=True
            )
        return self.__mset

    ##########

    def add_tags(self, *tags):
        """add a tags to the report"""
        for tag in tags:
            logger.debug(f"adding tag {tag} to report {self.id}")
            path = self.gen_path('tags', tag.lower())
            open(path, 'w').close()

    @property
    def tags(self):
        """list of report tags

        Tags are normalized to all lower case.

        """
        try:
            tags = [tag.lower() for tag in os.listdir(self.gen_path('tags'))]
        except FileNotFoundError:
            tags = []
        tags += self._git_tags()
        return sorted(tags)

    def is_valid(self):
        """returns True if current report version has a "valid" tag"""
        for tag in self.tags:
            if tag.startswith("valid"):
                return True
        return False

    def was_exported(self):
        """returns gpstime of the export tag, or False if not available"""
        for tag in self.tags:
            if tag.startswith("exported"):
                try:
                    return _util.parse_timestamp(tag.split('-')[1])
                except IndexError:
                    return True
        return False

    ##########

    def __get_sens_mcmc_map_file(self):
        return self.gen_path(
            "sensing_mcmc_map.json"
        )

    def get_sens_mcmc_results(self):
        """sensing function free parameters from report MCMC files

        returns dictionary of parameters

        """
        map_file = self.__get_sens_mcmc_map_file()
        with open(map_file) as f:
            data = json.load(f)
        data = list(data.values())[0]
        mcmc_map = data['mcmc_map_vals']
        params = {
            'map': {
                # optical gain (counts / m)
                'Hc': mcmc_map[0],
                # cavity pole frequency
                'Fcc': mcmc_map[1],
                # optical spring frequency
                'Fs': mcmc_map[2],
                # optical spring quality factor
                'Qs': mcmc_map[3],
                # residual time delay
                'tau_C': mcmc_map[4],
                },
            # was optical spring used in fit
            'is_anti_spring': not bool(data['model_config']['sensing']['is_pro_spring']),
            'fmin': data['fmin'],
            'fmax': data['fmax'],
        }
        return params

    def __get_act_mcmc_map_file(self, stage, optic):
        return self.gen_path(
            f'actuation_{stage}_{optic}_mcmc_map.json'
        )

    def get_act_mcmc_results(self):
        """actuation function free parameters from report MCMC files

        Returns
        -------
        params : dict
            Dictionary of parameters taken from MCMC results of the
            actuation function. The keys are of the form '<stage>/<optic>' and
            will be populated depending on the actuation stages and optics
            enabled as part of the current report. Each value in `params` is
            a dictionary with the following keys: 'map', 'fmin', 'fmax', and
            'Npct_scale'. The 'map' refers to the MCMC maximum a posteriori
            values and takes the form of a dictionary with 'H_A' and 'tau_A'
            as its keys. The lower and upper bounds of the MCMC fit range
            are specified in 'fmin' and 'fmax', respectively. The scale
            by which to multiply the normalized actuation frequency response
            to get to Newtons per count is included in the value paired with
            'scale_to_Npct'. This is the output of the corresponding stage's
            `<stage>_dc_gain_<drive unit>pct()` function, where drive unit is
            `A` for the top two stages and `V2` for the test stage.


        """
        act_config = self.config['Actuation']
        params = {}

        # map stages to corresponding N/ct scaling factors
        scale_method_names = {k: v for k, v in
                              zip(['L1', 'L2', 'L3'],
                                  ['uim_dc_gain_Apct',
                                   'pum_dc_gain_Apct',
                                   'tst_dc_gain_V2pct'])}
        # loop over optics/stages defined in config
        for k_stage, v_stage in act_config.items():
            if k_stage == 'params':
                continue
            for k_optic, v_optic in v_stage.items():
                if k_optic == 'params':
                    continue
                armact = getattr(self.model.actuation,
                                 f'{k_optic[-1].lower()}arm')
                scale_to_Npct = getattr(armact, scale_method_names[k_stage])()
                map_file = self.__get_act_mcmc_map_file(k_stage, k_optic)
                with open(map_file) as f:
                    map_data = json.load(f)
                map_data = list(map_data.values())[0]
                mcmc_map_vals = map_data['mcmc_map_vals']

                mcmc_map = {
                    'H_A': mcmc_map_vals[0],
                    'tau_A': mcmc_map_vals[1]
                }

                params['/'.join([k_stage, k_optic])] = {
                    'map': mcmc_map,
                    'fmin': map_data['fmin'],
                    'fmax': map_data['fmax'],
                    'Npct_scale': scale_to_Npct
                }

        return params

    def gen_free_params_ini_dict(self):
        """generate dictionary of pydarm ini parameters from MCMC results

        This output can be applied directly to the pydarm config
        object to update.

        """
        params = {}
        sens_params = self.get_sens_mcmc_results()['map']
        params['sensing'] = {
            'coupled_cavity_optical_gain': sens_params['Hc'],
            'coupled_cavity_pole_frequency': sens_params['Fcc'],
            'detuned_spring_frequency': sens_params['Fs'],
            'detuned_spring_Q': sens_params['Qs'],
            # FIXME: where is the time delay tau_C ??
        }
        for label, mcmc_params in self.get_act_mcmc_results().items():
            stage, optic = label.split('/')
            # FIXME: bad heuristic
            arm = optic[1].lower()
            section = f'actuation_{arm}_arm'
            var = {
                'L1': 'uim_NpA',
                'L2': 'pum_NpA',
                'L3': 'tst_NpV2',
            }[stage]
            if section not in params:
                params[section] = {}
            val = str(mcmc_params['map']['H_A'])
            params[section][var] = val
        return params

    ##########

    def _get_meas_obj(self, name, mtype):
        """wrapper to load Measurement object from mset"""
        path = self.mset.measurements[name][mtype]
        logger.debug(f"loading measurement: {name}/{mtype}...")
        try:
            return Measurement(path)
        except Exception as e:
            raise RuntimeError(f"could not parse measurment file: {path}") from e

    def process_sensing(self):
        """process sensing function measurements

        """
        name = 'Sensing'

        loopmeas = self._get_meas_obj(name, 'loop')
        pcalmeas = self._get_meas_obj(name, 'pcal')

        avail_channels_A, avail_channels_B = loopmeas.get_set_of_channels()
        avail_channels = avail_channels_A | avail_channels_B

        DARM_IN2_ch_opts = [f'{self.IFO}:LSC-DARM1_IN2', f'{self.IFO}:LSC-DARM_IN2']
        DARM_EXC_ch_opts = [f'{self.IFO}:LSC-DARM1_EXC', f'{self.IFO}:LSC-DARM_EXC']
        DARM_IN2_ch = set(DARM_IN2_ch_opts) & set(avail_channels_A)
        DARM_EXC_ch = set(DARM_EXC_ch_opts) & set(avail_channels)

        avail_channels_A, avail_channels_B = pcalmeas.get_set_of_channels()
        avail_channels = avail_channels_A | avail_channels_B

        PCALY_RX_ch_opts = [f'{self.IFO}:CAL-PCALY_RX_PD_OUT_DQ', f'{self.IFO}:CAL-PCALY_RX_PD_OUT']
        DARM_IN1_ch_opts = [f'{self.IFO}:LSC-DARM_IN1_DQ', f'{self.IFO}:LSC-DARM_IN1']

        PCALY_RX_ch = set(PCALY_RX_ch_opts) & set(avail_channels_A)
        DARM_IN1_ch = set(DARM_IN1_ch_opts) & set(avail_channels)

        for ch_opts in [DARM_IN2_ch, DARM_EXC_ch, PCALY_RX_ch, DARM_IN1_ch]:
            if len(ch_opts) > 1:
                raise Exception(f"Multiple channels available for same purpose: {ch_opts}")
            elif len(ch_opts) < 1:
                raise Exception("Channel not found")

        DARM_IN2_ch, DARM_EXC_ch, PCALY_RX_ch, DARM_IN1_ch = [
            list(ch)[0] for ch
            in [DARM_IN2_ch, DARM_EXC_ch, PCALY_RX_ch, DARM_IN1_ch]
        ]

        # This is a workaround to get the actual gps times for each measurement
        # Weird as it seems, this is done by running get_raw_tf().
        # The measurement object is initialized with gps_time None
        # because gps_time can only be accessed after getting the transfer fn.
        # See notes on pydarm Measurement object class.
        # On the plus side, I *think* that already supports xml and hdf5.
        loopmeas.get_raw_tf(DARM_IN2_ch, DARM_EXC_ch)
        pcalmeas.get_raw_tf(PCALY_RX_ch, DARM_IN1_ch)

        meas_gps = max(pcalmeas.gps_time, loopmeas.gps_time)
        timestamp = _util.gen_timestamp(gpstime.parse(meas_gps))

        processed = ProcessSensingMeasurement(
            self.model_file,
            loopmeas,
            pcalmeas,
            # FIXME: move these into the config
            (DARM_IN2_ch, DARM_EXC_ch),
            (PCALY_RX_ch, DARM_IN1_ch),
            self.config['Sensing']['params']['coh_thresh_loop'],
            self.config['Sensing']['params']['coh_thresh_pcal'],
            json_results_file=self.__get_sens_mcmc_map_file(),
        )

        return processed, timestamp

    def process_actuation(self):
        """process sensing function measurements

        """
        ref_pcal_name = self.model.pcal.pcal_filter_bank.rstrip("_PD")

        processed_dict = {}

        for stage, sdict in self.config['Actuation'].items():
            if stage == 'params':
                continue

            for optic, odict in sdict.items():
                if optic == 'params':
                    continue
                if optic in ['EX', 'EY', 'IX', 'IY']:
                    opt = f'{optic[0]}TM{optic[-1]}'

                name = f'Actuation/{stage}/{optic}'

                if name not in self.mset.measurements:
                    continue

                loopmeas = self._get_meas_obj(name, 'loop')
                pcalmeas = self._get_meas_obj(name, 'pcal')

                arm = optic[-1].lower()

                avail_channels_A, avail_channels_B = loopmeas.get_set_of_channels()
                avail_channels = avail_channels_A | avail_channels_B

                CAL_EXC_ch_opts = [
                    f'{self.IFO}:SUS-{opt}_{stage}_CAL_EXC',
                    f'{self.IFO}:SUS-{opt}_{stage}_TEST_L_EXC',
                ]
                DARM_IN1_ch_opts = [
                    f'{self.IFO}:LSC-DARM_IN1_DQ',
                    f'{self.IFO}:LSC-DARM_IN1_DQ',
                ]
                CAL_EXC_ch = set(CAL_EXC_ch_opts) & set(avail_channels_A)
                DARM_IN1_ch = set(DARM_IN1_ch_opts) & set(avail_channels)

                avail_channels_A, avail_channels_B = pcalmeas.get_set_of_channels()
                avail_channels = avail_channels_A | avail_channels_B

                CAL_REFPD_ch_opts = [
                    f'{self.IFO}:CAL-{ref_pcal_name}_PD_OUT_DQ',
                    f'{self.IFO}:CAL-{ref_pcal_name}_PD_OUT',
                ]
                CAL_REFPD_ch = set(CAL_REFPD_ch_opts) & set(avail_channels_A)
                DARM_IN1_ch_opts = [
                    f'{self.IFO}:LSC-DARM_IN1_DQ',
                    f'{self.IFO}:LSC-DARM_IN1',
                ]
                DARM_IN1_ch = set(DARM_IN1_ch_opts) & set(avail_channels)

                for ch_opts, ch_name in zip([CAL_EXC_ch, DARM_IN1_ch, CAL_REFPD_ch, DARM_IN1_ch],
                                            ["CAL_EXC_ch", "DARM_IN1_ch",
                                             "CAL_REFPD_ch", "DARM_IN1_ch"]):
                    if len(ch_opts) > 1:
                        raise Exception(f"Multiple channels available for same purpose: {ch_opts}")
                    elif len(ch_opts) < 1:
                        raise Exception(f"Channel not found: {ch_name}")

                CAL_EXC_ch, DARM_IN1_ch, CAL_REFPD_ch, DARM_IN1_ch = [
                    list(ch)[0] for
                    ch in [CAL_EXC_ch, DARM_IN1_ch, CAL_REFPD_ch, DARM_IN1_ch]
                ]

                loopmeas.get_raw_tf(CAL_EXC_ch, DARM_IN1_ch)
                pcalmeas.get_raw_tf(CAL_REFPD_ch, DARM_IN1_ch)

                meas_gps = max(pcalmeas.gps_time, loopmeas.gps_time)
                timestamp = _util.gen_timestamp(gpstime.parse(meas_gps))

                processed = ProcessActuationMeasurement(
                    self.model_file,
                    f'actuation_{arm}_arm',
                    loopmeas,
                    pcalmeas,
                    # FIXME: move these into config
                    (CAL_EXC_ch, DARM_IN1_ch),
                    (CAL_REFPD_ch, DARM_IN1_ch),
                    self.config['Actuation'][stage][optic]['params']['coh_thresh_loop'],
                    self.config['Actuation'][stage][optic]['params']['coh_thresh_pcal'],
                    json_results_file=self.__get_act_mcmc_map_file(stage, optic),
                )

                processed_dict[name] = (processed, timestamp)

        return processed_dict

    def process_broadband(self):
        """process broadband measurements
        """
        name = 'BroadBand'

        tfmeas = self._get_meas_obj(name, 'pcal')
        avail_channels_A, avail_channels_B = tfmeas.get_set_of_channels()
        avail_channels = avail_channels_A | avail_channels_B

        PCALY_RX_ch_opts = [f'{self.IFO}:CAL-PCALY_RX_PD_OUT_DQ',
                            f'{self.IFO}:CAL-PCALY_RX_PD_OUT']

        DELTAL_ch_opts = [f'{self.IFO}:CAL-DELTAL_EXTERNAL_DQ']

        PCALY_RX_ch = set(PCALY_RX_ch_opts) & set(avail_channels_A)
        DELTAL_ch = set(DELTAL_ch_opts) & set(avail_channels)

        for ch_opts in [PCALY_RX_ch, DELTAL_ch]:
            if len(ch_opts) > 1:
                raise Exception(f"Multiple channels available for same purpose: {ch_opts}")
            elif len(ch_opts) < 1:
                raise Exception("Channel not found")

        PCALY_RX_ch, DELTAL_ch = [
            list(ch)[0] for ch
            in [PCALY_RX_ch, DELTAL_ch]
        ]

        freqs, tf, _, _ = tfmeas.get_raw_tf(PCALY_RX_ch, DELTAL_ch)
        meas_gps = tfmeas.gps_time
        timestamp = _util.gen_timestamp(gpstime.parse(meas_gps))

        corr = self.calcs.deltal_ext_pcal_correction(freqs, endstation=False,
                                                     include_dewhitening=True,
                                                     arm='REF',
                                                     include_whitening=True)

        processed = tf * corr
        return freqs, processed, timestamp

    def load_measurements(self):
        """load and process sensing and actuation function measurements

        (ProcessedMeasurement, timestamp) tuples will be stored in the
        self.measurements dict.

        """
        self.measurements = self.process_actuation()
        self.measurements['Sensing'] = self.process_sensing()

    @staticmethod
    def default_path(report_id):
        """return the default path for a report with a given ID"""
        return os.path.join(
            CAL_REPORT_ROOT,
            report_id
        )

    @classmethod
    def create(cls, mset, config_file, model_file, path=None):
        """create a report from a measurement set, config file, and model file

        The report ID will be determined from the measurement set.  If
        a path is not provided, a default path in CAL_REPORT_ROOT will
        be used.

        """
        report_id = mset.id
        logger.debug(f"report id: {report_id}")
        if path is None:
            path = Report.default_path(report_id)
        logger.debug(f"report path: {path}")
        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, 'tags'), exist_ok=True)
        # write the report ID to a file
        with open(os.path.join(path, 'id'), 'w') as f:
            f.write(f"{report_id}\n")
        # create directory and export measurement set
        logger.debug(f"exporting mset: {mset}")
        # copy measurement files to report path
        mset.export(os.path.join(path, 'measurements'))
        # copy in mset config file
        logger.debug(f"copying config: {config_file}")
        try:
            shutil.copy(
                config_file,
                os.path.join(path, DEFAULT_CONFIG_FNAME),
            )
        except shutil.SameFileError:
            logger.debug("Skipped copy: same file")
        # copy in model file
        logger.debug(f"copying model: {model_file}")
        try:
            shutil.copy(
                model_file,
                os.path.join(path, DEFAULT_MODEL_FNAME),
            )
        except shutil.SameFileError:
            pass
        return cls(path)

    @classmethod
    def find(cls, report_id='last'):
        """get the report with given report ID from the CAL_REPORT_ROOT

        If `report_id` is 'last' or 'latest', the most recent report
        path will be returned.  If the specified report ID resolves to
        an existing directory, it will be assumed to be a report
        directory.  Otherwise an error will be throw if a report with
        the specified ID could not be found in the default path.

        """
        if report_id in ['last', 'latest']:
            report_list = list_reports(valid_only=False)
            if len(report_list) == 0:
                raise FileNotFoundError("no reports found!")
            return report_list[0]
        if os.path.exists(report_id):
            return cls(report_id)
        try:
            _util.parse_timestamp(report_id)
        except ValueError:
            gt = gpstime.parse(report_id)
            report_id = _util.gen_timestamp(gt)
        path = os.path.join(
            CAL_REPORT_ROOT,
            report_id
        )
        if not os.path.exists(path):
            raise FileNotFoundError(f"could not find report '{report_id}'.")
        return cls(path)


def list_reports(
        chronological=False, valid_only=True, exported_only=False,
        before=None, after=None,
):
    """return a list of reports, in reverse chronological order

    Reports are found in the CAL_REPORT_DIR directory.  The first
    report in the list is the most recent.  If `chronological=True`
    the report list will be in chronological order.

    By default only valid reports are returned.  If `valid_only` is
    False, invalid reports will also be included.

    If `exported_only` is True then only exported reports will be
    returned.

    `before` and `after` are time filters that filter for only reports
    from before or after the times specified, respectively.  `before`
    and `after` should be dateime or gpstime objects.

    """
    if before and after:
        assert before > after
    reports = []
    for r in os.listdir(CAL_REPORT_ROOT):
        # skip all dot files/directories
        if r[0] == '.':
            continue
        # skip the special "last-exported" report
        if r == 'last-exported':
            continue
        path = os.path.join(CAL_REPORT_ROOT, r)
        try:
            report = Report(path)
        except Exception as e:
            logger.warning(f"WARNING: skipping report with error: {path}: {e}")
            continue
        if r != report.id:
            logger.warning(f"WARNING: skipping improperly named report: {path}")
            continue
        if before and report.id_gpstime() > before:
            continue
        if after and report.id_gpstime() < after:
            continue
        if valid_only and not report.is_valid():
            continue
        if exported_only and not report.was_exported():
            continue
        reports.append(report)
    return sorted(
        reports,
        key=lambda report: report.id_gpstime(),
        reverse=not chronological,
    )
