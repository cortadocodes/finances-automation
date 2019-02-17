import sys
import datetime as dt
import math

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


THIS_MODULE = sys.modules[__name__]


def get_available_analyses():
    """ Get available analyses as a dictionary.

    :return dict:
    """
    analysis_names = {
        'calculate_category_totals',
        'calculate_category_averages',
        'calculate_category_totals_across_accounts',
        'plot_balance'
    }

    return {
        analysis_name: getattr(THIS_MODULE, analysis_name)
        for analysis_name in analysis_names
    }


def calculate_category_totals(table, categories, start_date, end_date, positive_expenses=True):
    """ Calculate the total flow of money in a table for a set of categories between two dates (inclusive).

    :param finances_automation.entities.Table table:
    :param dict(str, list) categories:
    :param datetime.date start_date:
    :param datetime.date end_date:
    :param bool positive_expenses:
    :return pd.DataFrame:
    """
    all_categories = categories['income'] + categories['expense']
    totals = pd.DataFrame(columns=all_categories)

    if positive_expenses:
        table.data[table.monetary_columns[1]] = - table.data[table.monetary_columns[1]]

    for category in all_categories:
        conditions = (
            (table.data['category'] == category)
            & (table.data[table.date_columns[0]] >= start_date)
            & (table.data[table.date_columns[0]] <= end_date)
        )

        category_total = (
            table.data[conditions][table.monetary_columns[0]].sum()
            + table.data[conditions][table.monetary_columns[1]].sum()
        )

        totals.loc[0, category] = round(category_total, 2)

    return totals


def _calculate_averages(table, categories, start_date, end_date, time_window=30):

    all_categories = categories['income'] + categories['expense']

    time_window = dt.timedelta(days=time_window)
    total_duration_available = end_date - start_date + dt.timedelta(1)
    number_of_windows = math.floor(total_duration_available / time_window)

    if time_window > total_duration_available:
        raise ValueError('time_window should be <= end_date - start_date')

    period_totals = pd.DataFrame(columns=all_categories)

    averages = pd.DataFrame(columns=(
        ['tables_analysed', 'analysis_type']
        + table_to_store.date_columns
        + all_categories
    ))

    start_dates = np.array([start_date + i * time_window for i in range(number_of_windows)])

    for i, start_date in enumerate(start_dates):
        end_date = start_date + time_window
        totals = calculate_category_totals(start_date, end_date)[all_categories]
        period_totals = period_totals.append(totals)

    for column in all_categories:
        averages.loc[0, column] = period_totals[column].mean().round(2)

    return averages


def calculate_category_totals_across_accounts(self, start_date=None, end_date=None, positive_expenses=True):
    self.export_type = 'csv'

    start_date = start_date or self.start_date
    end_date = end_date or self.end_date

    columns = (self.table_to_store.date_columns + ['tables_analysed'] + self.all_categories)
    columns.remove('credit_card')
    totals = pd.DataFrame(columns=columns)

    for category in self.all_categories:

        category_total = 0

        for table in self.tables_to_analyse:

            conditions = (
                (table.data['category'] == category)
                & (table.data[table.date_columns[0]] >= start_date)
                & (table.data[table.date_columns[0]] <= end_date)
            )

            table_category_total = (
                table.data[conditions][table.monetary_columns[0]].sum()
                - table.data[conditions][table.monetary_columns[1]].sum()
            )

            if positive_expenses:
                if category in self.categories['expense']:
                    table_category_total = - table_category_total

            category_total += table_category_total

        totals.loc[0, category] = round(category_total, 2)

    return totals


def _plot_balance(table, start_date, end_date):

    dates = table.data[table.date_columns[0]]
    balance = table.data['balance']

    dates_sorted, balance_sorted = zip(*sorted(zip(dates, balance)))

    figure = plt.figure(figsize=(12, 8))
    plt.plot(dates_sorted, balance_sorted)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Balance / £', fontsize=16)
    plt.title(
        'Balance of {} between {} and {}'.format(
            table.name, start_date, end_date
        ),
        fontsize=20
    )

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(0, 30, 5)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.tick_params(axis='both', which='both', labelsize=14)

    plt.show()

    return figure