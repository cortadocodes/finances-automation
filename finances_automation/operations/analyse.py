import datetime as dt

import pandas as pd

from finances_automation.entities.database import Database
from finances_automation import configuration as conf


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
        self.totals = {}

        self.table_to_analyse = table_to_analyse
        self.table_to_store = table_to_store

        self.income_categories = conf.INCOME_CATEGORIES
        self.expense_categories = conf.EXPENSE_CATEGORIES

        self.start_date = dt.datetime.strptime(start_date, self.table_to_analyse.date_format).date()
        self.end_date = (
            dt.datetime.strptime(end_date, self.table_to_analyse.date_format).date()
            + dt.timedelta(1)
        )

    def load_from_database(self):
        self.db.start()

        data_query = (
            """ SELECT * FROM {0}
            WHERE {1} > %s AND {1} < %s;
            """
            .format(self.table_to_analyse.name, self.table_to_analyse.date_column)
        )

        dates = self.start_date, self.end_date

        data = self.db.execute_statement(data_query, dates, output_required=True)

        self.data = pd.DataFrame(
            data, columns=self.table_to_analyse.schema.keys()
        ).astype(dtype={column: float for column in self.table_to_analyse.monetary_columns})

    def calculate_totals(self, positive_expenses=True):
        all_categories = self.income_categories + self.expense_categories
        self.totals = pd.DataFrame(columns=all_categories)

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


    def store_in_database(self):
        self.db.start()

        rows = list(self.totals.columns)
        values = tuple(self.totals.iloc[0])

        operation = (
            """INSERT INTO {} ({}) VALUES ({});"""
            .format(
                self.table_to_store.name,
                ', '.join(['{}'] * len(rows)),
                ', '.join(['%s'] * len(rows))
            )
            .format(*rows)
        )

        self.db.execute_statement(operation, values)

        self.db.stop()