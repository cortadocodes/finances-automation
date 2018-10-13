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

    def clean(self, monetary_columns):
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.data.drop_duplicates(inplace=True)
        self.remove_unwanted_characters(monetary_columns)
        self.convert_negative_values(monetary_columns)

    def remove_unwanted_characters(self, monetary_columns):
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace('£', '').str.replace(',', '')

    def convert_negative_values(self, monetary_columns):
        negatives_values = r'\((\d*\.*\d*)\)'
        replacement = r'-\1'
        for column in monetary_columns:
            self.data[column] = self.data[column].str.replace(negatives_values, replacement)


DB_LOCATION = os.path.join('..', 'data', 'database_cluster')
STATEMENT_LOCATION = os.path.join('..', 'data', 'example_statement.csv')


p = Parser('finances', 'Marcus1', DB_LOCATION, STATEMENT_LOCATION)
p.read(header=3)
p.clean(monetary_columns=['Money in', 'Money Out', 'Balance'])
