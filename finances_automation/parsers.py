import os

import pandas as pd

from finances_automation.database import Database


class parser:

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

    def clean(self):
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.data.drop_duplicates(inplace=True)

    def parse_negative_values(self):
        pass


DB_LOCATION = os.path.join('..', 'data', 'database_cluster')
STATEMENT_LOCATION = os.path.join('..', 'data', 'example_statement.csv')


p = parser('finances', 'Marcus1', DB_LOCATION, STATEMENT_LOCATION)
p.read(header=3)
p.clean()
