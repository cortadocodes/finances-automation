import sys

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
import pandas as pd


THIS_MODULE = sys.modules[__name__]

ANALYSIS_NAMES_AND_EXPORT_TYPES = {
    THIS_MODULE.calculate_category_totals.__name__: '.csv',
    THIS_MODULE.plot_balance.__name__: '.png'
}

ANALYSES_EXCLUDED_FROM_STORAGE = THIS_MODULE.plot_balance.__name__,


def get_available_analyses():
    """ Get available analyses as a dictionary.

    :return dict:
    """
    return {
        analysis_name: getattr(THIS_MODULE, analysis_name)
        for analysis_name in ANALYSIS_NAMES_AND_EXPORT_TYPES.keys()
    }

def get_analysis(analysis_type):
    """ Get the chosen analysis method, raising an error message if it is invalid.

    :param str analysis_type:
    :raise ValueError:
    :return callable:
    """
    available_analyses = get_available_analyses()

    if analysis_type in available_analyses:
        return available_analyses[analysis_type]

    raise ValueError(
        'Invalid analysis chosen; available analyses are: {}'
        .format(', '.join(available_analyses.keys()))
    )

def calculate_category_totals(table, categories, start_date, end_date, *args, **kwargs):
    """ Calculate the total flow of money in a transaction table for a set of categories between two dates (inclusive).

    :param finances_automation.entities.Table table:
    :param dict(str, list) categories:
    :param datetime.date start_date:
    :param datetime.date end_date:
    :param bool positive_expenses:
    :return pd.DataFrame:
    """
    all_categories = categories['income'] + categories['expense']
    totals = pd.DataFrame(columns=all_categories)

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


def plot_balance(table, start_date, end_date, show_plot=True, *args, **kwargs):
    """ Plot the balance of a transaction table between the start and end dates inclusively.

    :param finances_automation.entities.table.Table table:
    :param datetime.date start_date:
    :param datetime.date end_date:
    :param bool show_plot:
    :return matplotlib.figure.Figure:
    """
    dates = table.data[table.date_columns[0]]
    balance = table.data['balance']
    sorted_dates, sorted_balance = zip(*sorted(zip(dates, balance)))

    figure = plt.figure(figsize=(12, 8))
    plt.plot(sorted_dates, sorted_balance)

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Balance / £', fontsize=16)
    plt.title('Balance of {} between {} and {}'.format(table.name, start_date, end_date), fontsize=20)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(0, 30, 5)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.tick_params(axis='both', which='both', labelsize=14)

    if show_plot:
        plt.show()

    return figure
