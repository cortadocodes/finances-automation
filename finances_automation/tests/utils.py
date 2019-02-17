import datetime as dt
import random

import pandas as pd


def generate_random_dates_in_range(start, end, number=10):
    """ Generate a specified number of random dates in an inclusive range. Dates can be repeated.

    :param datetime.date start:
    :param datetime.date end:
    :param int number:

    :return list(datetime.date):
    """
    dates = list(date.date() for date in pd.date_range(start, end))
    return [random.choice(dates) for _ in range(number)]


def generate_random_dates_out_of_range(start, end, number=10, day_window=30):
    """ Generate a specified number of random date outside of an inclusive range. Dates can be repeated.

    :param datetime.date start:
    :param datetime.date end:
    :param int number:
    :param int day_window:

    :return list(datetime.date):
    """
    dates_less_than_range = [
        date.date()
        for date in pd.date_range(start - dt.timedelta(day_window), start - dt.timedelta(1))
    ]
    dates_more_than_range = [
        date.date()
        for date in pd.date_range(end + dt.timedelta(1), end + dt.timedelta(day_window))
    ]

    return [random.choice(dates_less_than_range + dates_more_than_range) for _ in range(number)]


def generate_random_edge_dates_in_range(start, end, number=10):
    """ Generate a specified number of dates at the very start or end of months in the date range given.

    :param datetime.date start:
    :param datetime.date end:
    :param int number:

    :return list(datetime.date):
    """
    edge_date_day_numbers = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    dates = list(date.date() for date in pd.date_range(start, end))
    edge_dates = [date for date in dates if date.day == edge_date_day_numbers[date.month]]
    return [random.choice(edge_dates) for _ in range(number)]