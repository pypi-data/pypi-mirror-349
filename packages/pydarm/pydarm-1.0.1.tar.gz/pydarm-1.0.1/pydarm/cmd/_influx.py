from functools import reduce

import yaml
import pandas as pd

from ligo.scald import utils
from ligo.scald.io import influx


class CalInfluxFetcher:

    def __init__(self, scald_config_file, IFO):

        with open(scald_config_file) as f:
            self.config = yaml.safe_load(f)

        backend = self.config['backends'][IFO]
        self.consumer = influx.Consumer(
            hostname=backend['hostname'],
            db=backend['db'],
            auth=backend['auth'],
            https=backend['https'],
            check_certs=backend['check_certs'],
        )

    @staticmethod
    def _format_influx_query(gps_start_time, gps_end_time, meas, fields, conditions=None):

        # Format measurements
        # This formats the measurement for a single measure only
        meas = f'"{meas}"'

        # Filter on GPS times
        # FIXME: a little clunky right now
        time_range = influx._format_influxql_conditions(start=gps_start_time, end=gps_end_time)
        if conditions is not None:
            conditions_suffix = ' AND '.join(conditions)
            all_conditions = time_range + ' AND ' + conditions_suffix
        else:
            all_conditions = time_range
        query = 'SELECT ' + ', '.join(fields) + f' FROM {meas} {all_conditions}'

        return query

    def _query(self, query):

        return influx._query_influx_data(
            self.consumer.client,
            self.consumer.db,
            query,
        )

    def fetch_data(self, gps_start_time, gps_end_time, meas, fields, conditions=None):
        """Fetches data from influxDB

        Parameters
        ----------
        gps_start_time: int
            Starting GPS time of the desired data segment
        gps_end_time: int
            Ending GPS time of the desired data segment
        meas: str
            Name of measurement to pull data for ('TF_mag',
            'TF_phase', etc.). Must be an existing measurement in the
            database specified during configuration.
        fields: str or list
            Name or names of fields associated with measurement meas
            to pull from influxDB. Field keys must be associated with
            meas.
        conditions: str or list
            List of additional filters/conditions to apply to query.
            NOTE: STRINGS MUST BE PASSED AS TRIPLE QUOTE STRINGS
            TO ACCORD WITH INFLUXDB FORMATTING.

        Returns
        -------
        dataframe: Pandas DataFrame
            Pandas DataFrame object with fields and meas as columns
            and time values as rows.

        """

        df_dict = {}
        for ms in meas:

            # Generate query and pull data for each measurement
            query = self._format_influx_query(
                gps_start_time, gps_end_time, ms, fields, conditions=conditions)
            cols, data = self._query(query)

            # Construct pandasDF
            dataframe = pd.DataFrame(data, columns=cols)

            # Change times from unix time to GPS times
            dataframe['time'] = dataframe['time'].apply(utils.unix_to_gps)

            # Reformat oscillator freq to be a float
            if 'oscillator_frequency' in dataframe.columns:
                dataframe['oscillator_frequency'].replace({'_': '.'}, inplace=True, regex=True)
                dataframe['oscillator_frequency'] = pd.to_numeric(dataframe['oscillator_frequency'])

            # Rename data column to be the specified measurement
            dataframe.rename(columns={'data': ms}, inplace=True)

            df_dict[ms] = dataframe

        # After all queries, merge dictionaries
        fields.remove('data')
        dataframe = reduce(lambda x, y: pd.merge(x, y, how='left',
                                                 on=fields), list(df_dict.values()))

        # FIXME: Not sure if this is the best way to do this
        self.dataframe = dataframe

        return dataframe
