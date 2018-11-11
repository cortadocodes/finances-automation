import os

import pandas as pd

from finances_automation.database import Database


class Categoriser:

    def __init__(self, db_name, db_location, db_user, income_categories, expense_categories):
        self.db = Database(db_name, db_location, db_user)
        self.data = None

        self.income_categories = income_categories
        self.expense_categories = expense_categories

    def load_from_database(self, table_name, table_headers):
        self.db.start()

        data_query = """SELECT * FROM {};""".format(table_name)

        self.data = pd.DataFrame(
            self.db.execute_statement(data_query, output_required=True),
            columns = table_headers
        )

    def select_categories(self):
        self.data['category_code'] = self.data.apply(
            self.select_category,
            axis=1
        )
        self.data['category'] = self.data.apply(
            self.convert_category_code,
            axis=1
        )

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
            print('{}: {}'.format(i, category), end='\n\n')

        print('Expense categories:')
        for j, category in enumerate(self.expense_categories):
            print('{}: {}'.format(i + j + 1, category), end='\n\n')

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

    def store_in_database(self, table_name):
        self.db.start()

        for i in range(len(self.data)):
            category_columns = ['id', 'category_code', 'category']
            data = list(self.data.iloc[i][category_columns])
            values = (data)

            operation = (
                """UPDATE {0}
                SET {2} = %s, {3} = %s
                """
                .format([table_name, category_columns[0], category_columns[1], category_columns[2]])
            )

            self.db.execute_statement(operation, values)

        self.db.stop()
