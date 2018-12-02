""" Contains parsers for reading in bank or card statements to be stored in the finances database.
"""

import pandas as pd

from finances_automation.scripts import configuration as conf
from finances_automation.database import Database
from finances_automation.table import Table


class BaseParser:

    def __init__(self, table, file):
        """ Initialise a BaseParser that reads a .csv file, cleans it and stores the result in a database.

        :param Table table: table to store data in
        :param str file: path to file to read in

        :var str db_name: name of database to store output in
        :var str db_location: location of that database
        :var st db_user: user to be used to access the database
        """
        self.check_types(table, file)

        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
        self.table = table
        self.file = file
        self.data = None


    @staticmethod
    def check_types(table, file):
        """ Check the variables passed in are of the correct type for BaseParser initialisation.

        :param any file: variable passed in as file argument
        :param Table table: table to store data in

        :raise: TypeError if any of the arguments are of the wrong type
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(file, str):
            raise TypeError('file should be a string.')

    def read(self):
        """ Read a statement at self.file, perform some operations and store it in self.data. This method should be
        overridden in inheriting classes.

        :raise NotImplementedError: if method not overridden by inheriting class
        """
        raise NotImplementedError

    def store_in_database(self):
        """ Store the parsed transactions in a database table.
        """
        self.db.start()

        for i in range(len(self.data)):
            columns = list(self.data.columns)
            values = tuple(self.data.iloc[i])

            operation = (
                """INSERT INTO {} ({}) VALUES ({});"""
                .format(
                    self.table.name,
                    ', '.join(['{}'] * len(columns)),
                    ', '.join(['%s'] * len(columns))
                )
                .format(*columns)
            )

            self.db.execute_statement(operation, values)

        self.db.stop()


class CSVCleaner(BaseParser):
    """ A parser that loads a .csv statement and cleans the data before storing it in the database.
    """

    def read(self, delimiter=',', header=0):
        """ Read the .csv statement at self.file into a pd.DataFrame object, and store it in self.data.

        :param str delimiter: column delimiter in self.file
        :param int header: row number that headers are on
        """
        self.data = pd.read_csv(self.file, delimiter=delimiter, header=header)

    def clean(self):
        """ Clean the statement's data by:

        * Dropping all-NaN rows and columns
        * Dropping duplicate rows
        * Converting column names to snake_case
        * Converting dates to the format specified in the configuration
        * Removing unwanted characters from monetary_columns
        * Converting the statement's notation for negative numbers to a standard minus sign
        """
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.data.drop_duplicates(inplace=True)

        self._convert_column_names()
        self._add_missing_database_table_columns()
        self._convert_dates()
        self._remove_unwanted_characters()
        self._convert_negative_values()

    def _convert_column_names(self):
        """ Convert column names to snake_case.
        """
        self.data.columns = self.data.columns.str.lower().str.replace(' ', '_')

    def _add_missing_database_table_columns(self):
        """ Add columns in the database table that are missing from the read-in file.
        """
        for column in self.table.schema.keys():
            if column not in self.data.columns and column != 'id':
                self.data[column] = 'NaN'

    def _convert_dates(self):
        """ Convert dates to the format specified in the configuration.
        """
        self.data[self.table.date_column] = pd.to_datetime(
            self.data[self.table.date_column],
            format=self.table.date_format
        )

    def _remove_unwanted_characters(self):
        """ Removing unwanted characters from monetary_columns.
        """
        for column in self.table.monetary_columns:
            self.data[column] = self.data[column].str.replace('£', '').str.replace(',', '')

    def _convert_negative_values(self):
        """ Convert (numbers) to standard negative notation.
        """
        negatives_values = r'\((\d*\.*\d*)\)'
        replacement = r'-\1'
        for column in self.table.monetary_columns:
            self.data[column] = self.data[column].str.replace(negatives_values, replacement)
