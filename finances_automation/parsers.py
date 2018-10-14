import os

import pandas as pd

from finances_automation.database import Database


class Parser:

    def __init__(self, db_name, db_location, db_user, file):
        self.check_types(file)

        self.db = Database(db_name, db_location, db_user)
        self.file = file
        self.data = None

        self.clean_successful = None
        self.storage_successful = None

    @staticmethod
    def check_types(file):
        if not isinstance(file, str):
            raise TypeError('file should be a string.')

    def read(self, delimiter=',', header=0):
        self.data = pd.read_csv(self.file, delimiter=delimiter, header=header)

    def clean(self, monetary_columns, date_column):
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.data.drop_duplicates(inplace=True)

        self.convert_column_names()
        self.convert_dates(date_column)
        self.remove_unwanted_characters(monetary_columns)
        self.convert_negative_values(monetary_columns)

    def convert_column_names(self):
        self.data.columns = self.data.columns.str.lower().str.replace(' ', '_')

    def remove_unwanted_characters(self, monetary_columns):
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace('£', '').str.replace(',', '')

    def convert_negative_values(self, monetary_columns):
        negatives_values = r'\((\d*\.*\d*)\)'
        replacement = r'-\1'
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace(negatives_values, replacement)

    def convert_dates(self, date_column):
        self.data[date_column] = pd.to_datetime(
            self.data[date_column],
            format='%d/%m/%Y'
        )

    def store_in_database(self, table_name):
        self.db.start()

        for i in range(len(self.data)):
            columns = list(self.data.columns)
            data = list(self.data.iloc[i])
            values = (data[0], data[1], data[2], data[3], data[4])

            operation = (
                """INSERT INTO {} ({}, {}, {}, {}, {})
                VALUES
                (%s, %s, %s, %s, %s);"""
                .format(table_name, columns[0], columns[1], columns[2], columns[3], columns[4])
            )

            self.db.execute_statement(operation, values)

        self.db.stop()


DB_LOCATION = os.path.join('..', 'data', 'database_cluster')
STATEMENT_LOCATION = os.path.join('..', 'data', 'example_statement.csv')
MONETARY_COLUMNS = ['money_in', 'money_out', 'balance']
DATE_COLUMN = 'date'


p = Parser('finances', DB_LOCATION, 'Marcus1', STATEMENT_LOCATION)
p.read(header=3)
p.clean(MONETARY_COLUMNS, DATE_COLUMN)
p.store_in_database('transactions')
