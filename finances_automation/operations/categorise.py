import datetime as dt

import pandas as pd

from finances_automation.entities.database import Database
from finances_automation import configuration as conf
from finances_automation.entities.table import Table


class Categoriser:

    def __init__(self, table, start_date, end_date):

        self.check_types(table, start_date, end_date)

        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
        self.data = None

        self.table = table

        self.income_categories = conf.INCOME_CATEGORIES
        self.expense_categories = conf.EXPENSE_CATEGORIES

        self.start_date = dt.datetime.strptime(start_date, self.table.date_format).date()
        self.end_date = (
            dt.datetime.strptime(end_date, self.table.date_format).date()
            + dt.timedelta(1)
        )

    @staticmethod
    def check_types(table, start_date, end_date):
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise TypeError('dates should be of type str.')

    def load_from_database(self):
        data = self.db.select_from(self.table, columns=['*'], conditions=[
            ('{} >='.format(self.table.date_column), self.start_date),
            ('AND {} <'.format(self.table.date_column), self.end_date)
        ])

        self.data = pd.DataFrame(data, columns=self.table.schema.keys())

    def select_categories(self):
        self.data['category_code'] = self.data.apply(self.select_category, axis=1)
        self.data['category'] = self.data.apply(self.convert_category_code, axis=1)

    def select_category(self, row):
        self.print_categories()
        print(str(row), end='\n\n')
        category = int(input('Category code: '))
        print('\n\n')

        return category

    def print_categories(self):
        print('=' * 45, end='\n\n')

        print('Income categories:')
        for i, category in enumerate(self.income_categories):
            print('{}: {}'.format(i, category))

        print('\nExpense categories:')
        for j, category in enumerate(self.expense_categories):
            print('{}: {}'.format(i + j + 1, category))
        print('\n')

    def convert_category_code(self, row):
        code = int(row['category_code'])
        income_length = len(self.income_categories)
        expense_length = len(self.expense_categories)

        if code < 0 | isinstance(code, float) | code >= expense_length + income_length:
            raise ValueError("Received a category code larger than the sum of the lengths of the category lists.")

        if code < income_length:
            category = self.income_categories[code]
        elif code < expense_length + income_length:
            category = self.expense_categories[code - income_length]

        return category

    def store_in_database(self):
        self.db.start()

        for i in range(len(self.data)):
            id = int(self.data.iloc[i, 0])
            data = tuple([
                int(self.data.iloc[i][self.table.category_columns[0]]),
                self.data.iloc[i][self.table.category_columns[1]]]
            )

            operation = (
                """
                UPDATE {0}
                SET {1} = %s, {2} = %s
                WHERE {0}.id = {3}
                """
                .format(
                    self.table.name,
                    self.table.category_columns[0],
                    self.table.category_columns[1],
                    id
                )
            )

            self.db.execute_statement(operation, data)

        self.db.stop()
