import datetime as dt

import numpy as np

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.repositories.categorise import CategoriseRepository


class Categoriser:

    def __init__(self, table, start_date, end_date, recategorise=False):

        self.check_types(table, start_date, end_date, recategorise)

        self.data = None
        self.table = table

        self.income_categories = conf.INCOME_CATEGORIES
        self.expense_categories = conf.EXPENSE_CATEGORIES
        self.adjustment_categories = conf.ADJUSTMENT_CATEGORIES

        self.start_date = dt.datetime.strptime(start_date, self.table.date_format).date()
        self.end_date = dt.datetime.strptime(end_date, self.table.date_format).date()

        self.recategorise = recategorise

    @staticmethod
    def check_types(table, start_date, end_date, recategorise):
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise TypeError('dates should be of type str.')
        if not isinstance(recategorise, bool):
            raise TypeError('recategorise should be boolean.')

    def load(self):
        self.data = CategoriseRepository().load(self.table, self.start_date, self.end_date)

    def store(self):
        CategoriseRepository().update(self.table, self.data)

    def select_categories(self):
        self.data['category_code'] = self.data.apply(self._select_category, axis=1)
        self.data['category'] = self.data.apply(self._convert_category_code, axis=1)

    def _select_category(self, row):
        if not self.recategorise:
            if not np.isnan(row['category_code']):
                return row['category_code']

        self._print_categories()

        relevant_columns = self.table.date_columns + ['description'] + self.table.monetary_columns
        print(row[relevant_columns], end='\n\n')

        category_code = int(input('Category code: '))
        print('\n\n')

        return category_code

    def _print_categories(self):
        print('=' * 45, end='\n\n')

        print('Income categories:')
        for i, category in enumerate(self.income_categories):
            print('{}: {}'.format(i, category))

        print('\nExpense categories:')
        for j, category in enumerate(self.expense_categories):
            print('{}: {}'.format(i + j + 1, category))

        print('\nAdjustment categories:')
        for k, category in enumerate(self.adjustment_categories):
            print('{}: {}'.format(i + j + k + 2, category))

        print('\n')

    def _convert_category_code(self, row):
        code = int(row['category_code'])
        income_length = len(self.income_categories)
        expense_length = len(self.expense_categories)
        adjustment_length = len(self.adjustment_categories)

        if code < 0 | isinstance(code, float) | code >= expense_length + income_length + adjustment_length:
            raise ValueError("Received a category code larger than the sum of the lengths of the category lists.")

        if code < income_length:
            category = self.income_categories[code]
        elif code < expense_length + income_length:
            category = self.expense_categories[code - income_length]
        elif code < expense_length + income_length + adjustment_length:
            category = self.adjustment_categories[code - income_length - expense_length]

        return category
