import datetime as dt
import random

import pandas as pd

from finances_automation.entities.table import Table
from finances_automation.operations.analyses import calculate_category_totals
from finances_automation.tests import utils


class TestCalculateCategoryTotals:

    @staticmethod
    def generate_random_test_table(dates, categories):
        """ Generate a test table of random transactions over a given set of dates and for a random set of the given
        categories.

        :param list(datetime.date) dates:
        :param dict categories:
        :return Table:
        """
        test_table = Table(
            name='name',
            type_='a_type',
            schema={
                'id': 'serial PRIMARY KEY',
                'date': 'DATE NOT NULL',
                'money_in': 'VARCHAR',
                'money_out': 'VARCHAR',
                'balance': 'DECIMAL',
                'category_code': 'DECIMAL',
                'category': 'VARCHAR'
            },
            monetary_columns={
                'money_in': 'money_in',
                'money_out': 'money_out',
                'balance': 'balance'
            },
            date_columns=['date'],
            date_format='%d/%m/%Y',
            category_columns=['category_code', 'category']
        )

        number_of_transactions = len(dates)

        test_table.data = pd.DataFrame(
            data={
                'date': dates,
                'money_in': [round(random.uniform(0, 1000), 2) for _ in range(number_of_transactions)],
                'money_out': [round(random.uniform(0, 500), 2) for _ in range(number_of_transactions)],
                'balance': [0 for _ in range(number_of_transactions)],
                'category': random.choices(categories['income'] + categories['expense'], k=number_of_transactions)
            }
        )

        return test_table

    def test_with_income_only(self):
        """ Test that a table of income transactions only is summed correctly.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        dates_in_range = utils.generate_random_dates_in_range(start_date, end_date, 10)
        categories = {
            'income': ['salary', 'other_income'],
            'expense': []
        }
        test_table = self.generate_random_test_table(dates_in_range, categories)

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            money_in = test_table.data[test_table.data['category'] == category]['money_in'].sum()
            money_out = test_table.data[test_table.data['category'] == category]['money_out'].sum()

            expected_total = round(money_in - money_out, 2)
            calculated_total = totals[category].iloc[0]

            assert calculated_total == expected_total

    def test_with_expense_only(self):
        """ Test that a table of income transactions only is summed correctly.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        dates_in_range = utils.generate_random_dates_in_range(start_date, end_date, 10)
        categories = {
            'income': ['salary', 'other_income'],
            'expense': ['charity_donations', 'food', 'clothing']
        }
        test_table = self.generate_random_test_table(dates_in_range, categories)

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            money_in = test_table.data[test_table.data['category'] == category]['money_in'].sum()
            money_out = test_table.data[test_table.data['category'] == category]['money_out'].sum()

            expected_total = round(money_in - money_out, 2)
            calculated_total = totals[category].iloc[0]

            assert calculated_total == expected_total

    def test_with_income_and_expense(self):
        """ Test that a table of income and expense transactions is summed correctly.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        dates_in_range = utils.generate_random_dates_in_range(start_date, end_date, 10)
        categories = {
            'income': [],
            'expense': ['charity_donations', 'food', 'clothing']
        }
        test_table = self.generate_random_test_table(dates_in_range, categories)

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            money_in = test_table.data[test_table.data['category'] == category]['money_in'].sum()
            money_out = test_table.data[test_table.data['category'] == category]['money_out'].sum()

            expected_total = round(money_in - money_out, 2)
            calculated_total = totals[category].iloc[0]

            assert calculated_total == expected_total

    def test_totals_zero_for_dates_outside_date_range(self):
        """ Test that a table of transactions outside the date range sum to zero inside the date range.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        dates_out_of_range = utils.generate_random_dates_out_of_range(start_date, end_date, 5)

        categories = {
            'income': ['salary', 'other_income'],
            'expense': ['charity_donations', 'food', 'clothing']
        }

        test_table = self.generate_random_test_table(dates_out_of_range, categories)

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            calculated_total = totals[category].iloc[0]
            assert calculated_total == 0

    def test_edge_dates_are_included(self):
        """ Test that dates on the inner edge of the date range are included.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        edge_dates = utils.generate_random_edge_dates_in_range(start_date, end_date, 5)

        categories = {
            'income': ['salary', 'other_income'],
            'expense': ['charity_donations', 'food', 'clothing']
        }

        test_table = self.generate_random_test_table(edge_dates, categories)

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            money_in = test_table.data[test_table.data['category'] == category]['money_in'].sum()
            money_out = test_table.data[test_table.data['category'] == category]['money_out'].sum()

            expected_total = round(money_in - money_out, 2)
            calculated_total = totals[category].iloc[0]

            assert calculated_total == expected_total

    def test_calculate_category_totals_with_dates_inside_and_outside_date_range(self):
        """ Test totals for the date range correctly exclude amounts for dates outside the range.

        :raise AssertionError:
        :return None:
        """
        start_date = dt.date(2019, 1, 1)
        end_date = dt.date(2019, 1, 31)

        dates_in_range = utils.generate_random_dates_in_range(start_date, end_date, 10)
        dates_out_of_range = utils.generate_random_dates_out_of_range(start_date, end_date, 5)

        categories = {
            'income': ['salary', 'other_income'],
            'expense': ['charity_donations', 'food', 'clothing']
        }

        test_table = self.generate_random_test_table(
            dates_in_range + dates_out_of_range,
            categories
        )

        totals = calculate_category_totals(test_table, categories, start_date, end_date)

        for category in categories['income'] + categories['expense']:
            money_in = test_table.data[
                (test_table.data['category'] == category)
                & (test_table.data['date'].isin(dates_in_range))
            ]['money_in'].sum()

            money_out = test_table.data[
                (test_table.data['category'] == category)
                & (test_table.data['date'].isin(dates_in_range))
            ]['money_out'].sum()

            expected_total = round(money_in - money_out, 2)
            calculated_total = totals[category].iloc[0]

            assert calculated_total == expected_total
