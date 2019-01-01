import datetime as dt
import math
import os

from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import numpy as np
import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.repositories.analyse import AnalyseRepository


class Analyser:

    analyses_excluded_from_storage = 'plot_balance',

    def __init__(self, table_to_analyse, table_to_store, analysis_type, start_date, end_date):
        """
        :param finances_automation.entities.table.Table table_to_analyse: table to analyse
        :param finances_automation.entities.table.Table table_to_store: table to store analysis in
        :param str start_date: date to start analysis at
        :param str end_date: date to end analysis at
        """
        self.check_types(table_to_analyse, table_to_store, analysis_type, start_date, end_date)

        self.analyses = {
            'totals': self._calculate_totals,
            'monthly_averages': self._calculate_averages,
            'plot_balance': self._plot_balance
        }

        self.table_to_analyse = table_to_analyse
        self.table_to_store = table_to_store

        self.analysis_type = analysis_type
        self.analysis = None
        self.export_type = None

        self.categories = conf.CATEGORIES
        self.all_categories = self.categories['income'] + self.categories['expense']

        self.start_date = dt.datetime.strptime(start_date, self.table_to_analyse.date_format).date()
        self.end_date = dt.datetime.strptime(end_date, self.table_to_analyse.date_format).date()

    @staticmethod
    def check_types(table_to_analyse, table_to_store, analysis_type, start_date, end_date):
        if not isinstance(table_to_analyse, Table):
            raise TypeError('table_to_analyse must be a Table.')
        if not (isinstance(table_to_store, Table) or table_to_store is None):
            raise TypeError('table_to_store must be a Table or None.')
        if not isinstance(analysis_type, str):
            raise TypeError('analysis_type must be a string.')
        if not isinstance(start_date, str):
            raise TypeError('start_date must be a string.')
        if not isinstance(end_date, str):
            raise TypeError('end_date must be a string.')

    def _load(self):
        self.table_to_analyse.data = AnalyseRepository().load(
            self.table_to_analyse, self.start_date, self.end_date
        )

    def _insert(self):
        AnalyseRepository().insert(self.analysis, self.table_to_store)

    def analyse(self):
        self._load()
        self.analysis = self.analyses[self.analysis_type]()

        if self.analysis_type not in self.analyses_excluded_from_storage:
            self._set_metadata()
            self._insert()

    def _calculate_totals(self, start_date=None, end_date=None, positive_expenses=True):
        self.export_type = 'csv'

        start_date = start_date or self.start_date
        end_date = end_date or self.end_date

        totals = pd.DataFrame(columns=(
            ['table_analysed', 'analysis_type']
            + self.table_to_store.date_columns
            + self.all_categories
        ))

        for category in self.all_categories:
            conditions = (
                (self.table_to_analyse.data['category'] == category)
                & (self.table_to_analyse.data[self.table_to_analyse.date_columns[0]] >= start_date)
                & (self.table_to_analyse.data[self.table_to_analyse.date_columns[0]] <= end_date)
            )

            category_total = (
                self.table_to_analyse.data[conditions][self.table_to_analyse.monetary_columns[0]].sum()
                - self.table_to_analyse.data[conditions][self.table_to_analyse.monetary_columns[1]].sum()
            )

            if positive_expenses:
                if category in self.categories['expense']:
                    category_total = - category_total

            totals.loc[0, category] = round(category_total, 2)

        return totals

    def _calculate_averages(self, time_window=30):
        self.export_type = 'csv'

        time_window = dt.timedelta(days=time_window)
        total_duration_available = self.end_date - self.start_date + dt.timedelta(1)
        number_of_windows = math.floor(total_duration_available / time_window)

        if time_window > total_duration_available:
            raise ValueError('time_window should be <= self.end_date - self.start_date')

        period_totals = pd.DataFrame(columns=self.all_categories)
        averages = pd.DataFrame(columns=(
            ['table_analysed', 'analysis_type']
            + self.table_to_store.date_columns
            + self.all_categories
        ))

        start_dates = np.array([self.start_date + i * time_window for i in range(number_of_windows)])

        for i, start_date in enumerate(start_dates):
            end_date = start_date + time_window
            totals = self._calculate_totals(start_date, end_date)[self.all_categories]
            period_totals = period_totals.append(totals)

        for column in self.all_categories:
            averages.loc[0, column] = period_totals[column].mean().round(2)

        return averages

    def _plot_balance(self):
        self.export_type = 'image'

        dates = self.table_to_analyse.data[self.table_to_analyse.date_columns[0]]
        balance = self.table_to_analyse.data['balance']

        dates_sorted, balance_sorted = zip(*sorted(zip(dates, balance)))

        figure = plt.figure(figsize=(12, 8))
        plt.plot(dates_sorted, balance_sorted)
        plt.xlabel('Date', fontsize=16)
        plt.ylabel('Balance / £', fontsize=16)
        plt.title(
            'Balance of {} between {} and {}'.format(
                self.table_to_analyse.name, self.start_date, self.end_date
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

    def _set_metadata(self):
        for date_column in self.table_to_store.date_columns:
            self.analysis[date_column] = pd.to_datetime(
                self.analysis[date_column],
                format=self.table_to_store.date_format
            )

        self.analysis['table_analysed'] = self.table_to_analyse.name
        self.analysis['start_date'] = self.start_date
        self.analysis['end_date'] = self.end_date
        self.analysis['analysis_datetime'] = dt.datetime.now()

    def export_analysis(self, path):
        if self.analysis is None:
            raise ValueError('Analysis must be carried out before being exported.')

        path = os.path.join(path, self.analysis_type)

        if not os.path.exists(path):
            os.makedirs(path)

        if self.export_type == 'csv':
            filename = '_'.join([self.table_to_analyse.name, str(dt.datetime.now()), '.csv'])
            self.analysis.to_csv(os.path.join(path, filename), index=False, encoding='utf-8')
        elif self.export_type == 'image':
            filename = '_'.join([self.table_to_analyse.name, str(dt.datetime.now()), '.png'])
            self.analysis.savefig(os.path.join(path, filename), format='png')
