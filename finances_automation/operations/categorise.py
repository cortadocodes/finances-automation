import datetime as dt

import numpy as np
import pandas as pd

from finances_automation import configuration as conf
from finances_automation.repositories import TransactionsRepository
from finances_automation.validation.categorise import categoriser_validator


class Categoriser:

    @categoriser_validator
    def __init__(self, table, start_date, end_date, recategorise=False):
        """ Intialise a Categoriser.

        :param finances_automation.entities.table.Table table:
        :param dt.date start_date:
        :param dt.date end_date:
        :param bool recategorise:
        :return None:
        """
        self.table = table
        self.table_repository = TransactionsRepository(self.table)

        self.categories = conf.categories

        self.start_date = dt.datetime.strptime(start_date, self.table.date_format).date()
        self.end_date = dt.datetime.strptime(end_date, self.table.date_format).date()

        self.recategorise = recategorise

        pd.set_option('max_colwidth', 200)
        pd.set_option('display.width', 1000)

    def select_categories(self):
        """ Select categories for the transactions in the table.

        :return None:
        """
        self.table_repository.load(self.start_date, self.end_date)

        self.table.data['category_code'] = self.table.data.apply(self._select_category, axis=1)
        self.table.data['category'] = self.table.data.apply(self._convert_category_code, axis=1)

        self.table_repository.update_categories()

    def _select_category(self, row):
        """ Set the category code for a table row.

        :param pd.Series row:
        :return int:
        """
        if not self.recategorise:
            if not np.isnan(row['category_code']):
                return row['category_code']

        self._print_categories()

        relevant_columns = self.table.date_columns + ['description'] + list(self.table.monetary_columns.values())
        print(row[relevant_columns], end='\n\n')

        category_code = int(input('Category code: '))
        print('\n\n')

        return category_code

    def _print_categories(self):
        """ Print the available categories.

        :return None:
        """
        i, j, k = 0, 0, 0

        print('=' * 45, end='\n\n')

        print('Income categories:')
        for i, category in enumerate(self.categories['income']):
            print('{}: {}'.format(i, category))

        print('\nExpense categories:')
        for j, category in enumerate(self.categories['expense']):
            print('{}: {}'.format(i + j + 1, category))

        print('\nAdjustment categories:')
        for k, category in enumerate(self.categories['adjustment']):
            print('{}: {}'.format(i + j + k + 2, category))

        print('\n')

    def _convert_category_code(self, row):
        """ Convert the category code of a table row to the human-readable category.

        :param pd.Series row:
        :return str:
        """
        category = None
        code = int(row['category_code'])

        income_length = len(self.categories['income'])
        expense_length = len(self.categories['expense'])
        adjustment_length = len(self.categories['adjustment'])

        is_invalid_code = (
            code < 0
            | isinstance(code, float)
            | code >= expense_length + income_length + adjustment_length
        )

        if is_invalid_code:
            raise ValueError('Received an invalid category_code: {}'.format(code))

        if code < income_length:
            category = self.categories['income'][code]
        elif code < expense_length + income_length:
            category = self.categories['expense'][code - income_length]
        elif code < expense_length + income_length + adjustment_length:
            category = self.categories['adjustment'][code - income_length - expense_length]

        return category
