import datetime as dt
import os

import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.repositories.analyse import AnalyseRepository


class Analyser:

    def __init__(self, table_to_analyse, table_to_store, analysis_type, start_date, end_date):
        """
        :param finances_automation.entities.table.Table table_to_analyse: table to analyse
        :param finances_automation.entities.table.Table table_to_store: table to store analysis in
        :param str start_date: date to start analysis at
        :param str end_date: date to end analysis at
        """
        self.check_types(table_to_analyse, table_to_store, analysis_type, start_date, end_date)

        self.data = None

        self.analyses = {
            'totals': self._calculate_totals
        }

        self.table_to_analyse = table_to_analyse
        self.table_to_store = table_to_store
        self.analysis_type = analysis_type

        self.income_categories = conf.INCOME_CATEGORIES
        self.expense_categories = conf.EXPENSE_CATEGORIES
        self.all_categories = self.income_categories + self.expense_categories

        self.start_date = dt.datetime.strptime(start_date, self.table_to_analyse.date_format).date()
        self.end_date = dt.datetime.strptime(end_date, self.table_to_analyse.date_format).date()

        self.analysis = pd.DataFrame(columns = (
            ['table_analysed', 'analysis_type']
            + self.table_to_store.date_columns
            + self.all_categories
        ))

    @staticmethod
    def check_types(table_to_analyse, table_to_store, analysis_type, start_date, end_date):
        if not isinstance(table_to_analyse, Table):
            raise TypeError('table_to_analyse must be a Table.')
        if not isinstance(table_to_store, Table):
            raise TypeError('table_to_store must be a Table.')
        if not isinstance(analysis_type, str):
            raise TypeError('analysis_type must be a string.')
        if not isinstance(start_date, str):
            raise TypeError('start_date must be a string.')
        if not isinstance(end_date, str):
            raise TypeError('end_date must be a string.')

    def load(self):
        self.data = AnalyseRepository().load(self.table_to_analyse, self.start_date, self.end_date)

    def store(self):
        AnalyseRepository().store(self.table_to_store, self.analysis)

    def analyse(self):
        self.analyses[self.analysis_type]()
        self._set_metadata()

    def _calculate_totals(self, positive_expenses=True):
        for category in self.all_categories:
            condition = self.data['category'] == category
            category_total = (
                self.data[condition][self.table_to_analyse.monetary_columns[0]].sum()
                - self.data[condition][self.table_to_analyse.monetary_columns[1]].sum()
            )

            if positive_expenses:
                if category in self.expense_categories:
                    category_total = - category_total

            self.analysis.loc[0, category] = round(category_total, 2)

    def _set_metadata(self):
        for date_column in self.table_to_store.date_columns:
            self.analysis[date_column] = pd.to_datetime(
                self.analysis[date_column],
                format=self.table_to_store.date_format
            )

        self.analysis['table_analysed'] = self.table_to_analyse.name
        self.analysis['analysis_type'] = self.analysis_type
        self.analysis['start_date'] = self.start_date
        self.analysis['end_date'] = self.end_date
        self.analysis['analysis_datetime'] = dt.datetime.now()

    def get_analysis_as_csv(self, path):
        if self.analysis is None:
            raise ValueError('Analysis must be carried out before being exported.')

        filename = '_'.join([self.table_to_analyse.name, str(dt.datetime.now()), '.csv'])
        full_path = os.path.join(path, self.analysis_type, filename)
        self.analysis.to_csv(full_path, index=False, encoding='utf-8')
