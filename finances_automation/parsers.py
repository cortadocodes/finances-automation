""" Contains parsers for reading in bank or card statements to be stored in the finances database.
"""

import pandas as pd

from finances_automation.scripts import configuration as conf
from finances_automation.database import Database


class Parser:

    def __init__(self, db_name, db_location, db_user, table_name, file):
        self.check_types(file)

        self.db = Database(db_name, db_location, db_user)
        self.file = file
        self.data = None

        self.table_name = table_name

        self.clean_successful = None
        self.storage_successful = None

    @staticmethod
    def check_types(file, table_name):
        if not isinstance(file, str):
            raise TypeError('file should be a string.')
        if not isinstance(table_name):
            raise TypeError('table_name should be a string.')

    def read(self, delimiter=',', header=0):
        """ Read the statement at self.file into a pd.DataFrame object, and store it in self.data.

        :param str delimiter: column delimiter in self.file
        :param int header: row number that headers are on
        """
        self.data = pd.read_csv(self.file, delimiter=delimiter, header=header)

    def clean(self, monetary_columns, date_column):
        """ Clean the statement's data by:
        * Dropping all-NaN rows and columns
        * Dropping duplicate rows
        * Converting column names to snake_case
        * Converting dates to the format specified in the configuration
        * Removing unwanted characters from monetary_columns
        * Converting the statement's notation for negative numbers to a standard minus sign

        :param list(str) monetary_columns: names of columns containing monetary amounts
        :param str date_column: name of date column
        """
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.data.drop_duplicates(inplace=True)

        self.convert_column_names()
        self.convert_dates(date_column)
        self.remove_unwanted_characters(monetary_columns)
        self.convert_negative_values(monetary_columns)

    def convert_column_names(self):
        """ Convert column names to snake_case.
        """
        self.data.columns = self.data.columns.str.lower().str.replace(' ', '_')

    def convert_dates(self, date_column):
        """ Convert dates to the format specified in the configuration.

        :param str date_column: name of date column
        """
        self.data[date_column] = pd.to_datetime(
            self.data[date_column],
            format=conf.DATE_FORMAT
        )

    def remove_unwanted_characters(self, monetary_columns):
        """ Removing unwanted characters from monetary_columns.

        :param list(str) monetary_columns: names of columns containing monetary amounts
        """
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace('£', '').str.replace(',', '')

    def convert_negative_values(self, monetary_columns):
        """ Convert (numbers) to standard negative notation.

        :param list(str) monetary_columns: names of columns containing monetary amounts
        """
        negatives_values = r'\((\d*\.*\d*)\)'
        replacement = r'-\1'
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace(negatives_values, replacement)

    def store_in_database(self):
        """ Store the parsed transactions in a database table.

        :param str table_name: name of table to store in
        """
        self.db.start()

        for i in range(len(self.data)):
            columns = list(self.data.columns)
            data = list(self.data.iloc[i])
            values = tuple(data)

            operation = (
                """INSERT INTO {} ({}, {}, {}, {}, {})
                VALUES
                (%s, %s, %s, %s, %s);"""
                .format(self.table_name, *columns)
            )

            self.db.execute_statement(operation, values)

        self.db.stop()
