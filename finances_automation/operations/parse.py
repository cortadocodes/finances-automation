""" Contains parsers for reading in bank or card statements to be stored in the finances database.
"""
import numpy as np
import pandas as pd

from finances_automation import configuration as conf
from finances_automation.repositories import BaseRepository
from finances_automation.validation.parse import base_parser_validator


class BaseParser:

    @base_parser_validator
    def __init__(self, table, file):
        """ Initialise a BaseParser that reads a .csv file, cleans it and stores the result in a database.

        :param finances_automation.entities.table.Table table: table to store data in
        :param str file: path to file to read in
        """
        self.table = table
        self.table_repository = BaseRepository(self.table)

        self.file = file

        self.data = None

    def _read(self, *args, **kwargs):
        """ Read a statement at self.file, perform some operations and store it in self.data.
        This method should be overridden in inheriting classes.

        :raise NotImplementedError: if method not overridden by inheriting class
        """
        raise NotImplementedError

    def parse(self):
        """ Parse the statement.

        :raise NotImplementedError: if method not overridden by inheriting class
        """
        raise NotImplementedError


class CSVParser(BaseParser):
    """ A parser that loads a .csv statement and cleans the data before storing it in the database.
    """
    def parse(self):
        """ Clean and store the statement.

        :param str delimiter: column delimiter in self.file
        :param int header: row number that headers are on
        :param list usecols: names or numbers of columns to use
        :param dict dtype: mapping of column name to type of data e.g. np.float64
        """
        self._read(**conf.parser)
        self._clean()
        self.table_repository.insert(self.data)

    def _read(self, delimiter, header, usecols, dtype):
        """ Read the .csv statement at self.file into a pd.DataFrame object, and store it in self.data.

        :param str delimiter: column delimiter in self.file
        :param int header: row number that headers are on
        :param list usecols: names or numbers of columns to use
        :param dict dtype: mapping of column name to type of data e.g. np.float64
        """
        self.data = pd.read_csv(
            self.file,
            delimiter=delimiter,
            header=header,
            usecols=usecols,
            dtype=dtype
        )

    def _clean(self):
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
        self._remove_unwanted_characters()
        self._convert_negative_values()
        self._enforce_column_types()

    def _convert_column_names(self):
        """ Convert column names to snake_case.
        """
        self.data.columns = self.data.columns.str.lower().str.replace(' ', '_')

    def _add_missing_database_table_columns(self):
        """ Add columns in the database table that are missing from the read-in file.
        """
        for column in self.table.schema.keys():
            if column not in self.data.columns and column != 'id':
                self.data[column] = np.nan

    def _remove_unwanted_characters(self):
        """ Removing unwanted characters from monetary_columns.
        """
        for column in self.table.monetary_columns.values():
            self.data[column] = (
                self.data[column].astype(str).str.replace('£', '').str.replace(',', '')
            )

    def _convert_negative_values(self):
        """ Convert (numbers) to standard negative notation.
        """
        negatives_values = r'\((\d*\.*\d*)\)'
        replacement = r'-\1'

        for column in self.table.monetary_columns.values():
            self.data[column] = self.data[column].str.replace(negatives_values, replacement)

    def _enforce_column_types(self):
        """ Convert dates to the format specified in the configuration.
        """
        for date_column in self.table.date_columns:
            self.data[date_column] = pd.to_datetime(
                self.data[date_column],
                format=self.table.date_format
            )

        self.data = self.data.astype(
            dtype={column: float for column in self.table.monetary_columns.values()}
        )
