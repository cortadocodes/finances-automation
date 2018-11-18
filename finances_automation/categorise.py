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
            columns=table_headers
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

    def store_in_database(self, table_name):
        self.db.start()

        category_columns = ['category_code', 'category']

        for i in range(len(self.data)):
            id = int(self.data.iloc[i, 0])
            data = tuple([int(self.data.iloc[i][category_columns[0]]), self.data.iloc[i][category_columns[1]]])

            operation = (
                """
                UPDATE {0}
                SET {1} = %s, {2} = %s
                WHERE {0}.id = {3}
                """
                .format(table_name, category_columns[0], category_columns[1], id)
            )

            self.db.execute_statement(operation, data)

        self.db.stop()
