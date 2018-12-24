import datetime as dt
import os

import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class Analyser:

    def __init__(self, table_to_analyse, table_to_store, start_date, end_date):
        """
        :param finances_automation.entities.table.Table table_to_analyse: table to analyse
        :param finances_automation.entities.table.Table table_to_store: table to store analysis in
        :param str start_date: date to start analysis at
        :param str end_date: date to end analysis at
        """
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
        self.data = None
        self.totals = None

        self.table_to_analyse = table_to_analyse
        self.table_to_store = table_to_store

        self.income_categories = conf.INCOME_CATEGORIES
        self.expense_categories = conf.EXPENSE_CATEGORIES

        self.start_date = dt.datetime.strptime(start_date, self.table_to_analyse.date_format).date()
        self.end_date = dt.datetime.strptime(end_date, self.table_to_analyse.date_format).date()

    def load_from_database(self):
        data = self.db.select_from(self.table_to_analyse, columns=['*'], conditions=[
            ('{} >='.format(self.table_to_analyse.date_columns[0]), self.start_date),
            ('AND {} <='.format(self.table_to_analyse.date_columns[0]), self.end_date),
        ])

        self.data = pd.DataFrame(
            data, columns=self.table_to_analyse.schema.keys()
        ).astype(dtype={column: float for column in self.table_to_analyse.monetary_columns})

    def calculate_totals(self, positive_expenses=True):
        all_categories = self.income_categories + self.expense_categories
        self.totals = pd.DataFrame(columns=['start_date', 'end_date'] + all_categories)

        for category in all_categories:
            condition = self.data['category'] == category
            category_total = (
                self.data[condition][self.table_to_analyse.monetary_columns[0]].sum()
                - self.data[condition][self.table_to_analyse.monetary_columns[1]].sum()
            )

            if positive_expenses:
                if category in self.expense_categories:
                    category_total = - category_total

            self.totals.loc[0, category] = round(category_total, 2)

        for date_column in self.table_to_store.date_columns:
            self.totals[date_column] = pd.to_datetime(
                self.totals[date_column],
                format=self.table_to_store.date_format
            )

        self.totals['start_date'] = self.start_date
        self.totals['end_date'] = self.end_date
        self.totals['analysis_date'] = dt.datetime.now()

    def get_totals_as_csv(self, path):
        if self.totals is None:
            raise ValueError('Totals must be calculated before being exported.')

        filename = '_'.join(['totals', self.table_to_analyse.name, str(dt.datetime.now()), '.csv'])

        self.totals.to_csv(os.path.join(path, filename), index=False)

    def store_in_database(self):
        self.db.insert_into(
            self.table_to_store,
            tuple(self.totals.columns),
            self.totals.itertuples(index=False)
        )
