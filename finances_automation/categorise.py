import datetime

import pandas as pd

from finances_automation.database import Database


class Categoriser:

    def __init__(self,
                 db_name,
                 db_location,
                 db_user,
                 table_name,
                 table_headers,
                 income_categories,
                 expense_categories,
                 category_columns,
                 date_column,
                 date_format,
                 start_date,
                 end_date):

        self.db = Database(db_name, db_location, db_user)
        self.data = None

        self.table_name = table_name
        self.table_headers = table_headers

        self.income_categories = income_categories
        self.expense_categories = expense_categories

        self.category_columns = category_columns

        self.date_column = date_column
        self.date_format = date_format
        self.start_date = datetime.datetime.strptime(start_date, self.date_format)
        self.end_date = datetime.datetime.strptime(end_date, self.date_format) + datetime.timedelta(1)


    def load_from_database(self):
        self.db.start()

        data_query = (
            """ SELECT * FROM {0}
            WHERE {1} > {2} AND {1} < {3};
            """
            .format(self.table_name, self.date_column, self.start_date, self.end_date)
        )

        data = self.db.execute_statement(data_query, output_required=True)
        self.data = pd.DataFrame(data, columns=self.table_headers)

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
            data = tuple([int(self.data.iloc[i][self.category_columns[0]]), self.data.iloc[i][self.category_columns[1]]])

            operation = (
                """
                UPDATE {0}
                SET {1} = %s, {2} = %s
                WHERE {0}.id = {3}
                """
                .format(self.table_name, self.category_columns[0], self.category_columns[1], id)
            )

            self.db.execute_statement(operation, data)

        self.db.stop()
