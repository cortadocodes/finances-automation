import datetime as dt
import os

import pandas as pd

from finances_automation import configuration as conf
from finances_automation.operations import analyses
from finances_automation.repositories import BaseRepository
from finances_automation.validation.analyse import analyser_validator


class Analyser:

    analyses_excluded_from_storage = 'plot_balance',

    @analyser_validator
    def __init__(self, analysis_type, tables_to_analyse, table_to_store, start_date, end_date):
        """
        :param list(finances_automation.entities.table.Table) tables_to_analyse: tables to analyse
        :param finances_automation.entities.table.Table table_to_store: table to store analysis in
        :param str analysis_type: name of analysis to carry out
        :param str start_date: date to start analysis at
        :param str end_date: date to end analysis at
        """
        self.analyses = {
            'totals': analyses.calculate_category_totals,
            'monthly_averages': analyses.calculate_category_averages,
            'totals_across_all_accounts': analyses.calculate_category_totals_across_accounts,
            'plot_balance': analyses.plot_balance
        }

        self.tables_to_analyse = tables_to_analyse
        self.table_to_store = table_to_store

        if isinstance(self.tables_to_analyse, list):
            self.tables_to_analyse_repositories = [BaseRepository(table) for table in self.tables_to_analyse]
            self.start_date = dt.datetime.strptime(start_date, self.tables_to_analyse[0].date_format).date()
            self.end_date = dt.datetime.strptime(end_date, self.tables_to_analyse[0].date_format).date()

            for repository in self.tables_to_analyse_repositories:
                repository.load(self.start_date, self.end_date)
        else:
            self.tables_to_analyse_repositories = BaseRepository(self.tables_to_analyse)
            self.start_date = dt.datetime.strptime(start_date, self.tables_to_analyse.date_format).date()
            self.end_date = dt.datetime.strptime(end_date, self.tables_to_analyse.date_format).date()
            self.tables_to_analyse_repositories.load(self.start_date, self.end_date)

        self.table_to_store_repository = BaseRepository(self.table_to_store)

        self.analysis_type = analysis_type
        self.analysis = None
        self.export_type = None

        self.categories = conf.categories
        self.all_categories = self.categories['income'] + self.categories['expense']

    def analyse(self):
        self.analysis = self.analyses[self.analysis_type]()

        if self.analysis_type not in self.analyses_excluded_from_storage:
            self._set_metadata()
            self.table_to_store_repository.insert(self.analysis)

    def _set_metadata(self):
        for date_column in self.table_to_store.date_columns:
            self.analysis[date_column] = pd.to_datetime(
                self.analysis[date_column],
                format=self.table_to_store.date_format
            )

        if isinstance(self.tables_to_analyse, list):
            self.analysis['tables_analysed'] = ';'.join([table.name for table in self.tables_to_analyse])
        else:
            self.analysis['tables_analysed'] = self.tables_to_analyse.name

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
            if isinstance(self.tables_to_analyse, list):
                filename = '_'.join(
                    [';'.join([table.name for table in self.tables_to_analyse]), str(dt.datetime.now()), '.csv']
                )
            else:
                filename = '_'.join(
                    [self.tables_to_analyse.name, str(dt.datetime.now()), '.csv']
                )

            self.analysis.to_csv(os.path.join(path, filename), index=False, encoding='utf-8')

        elif self.export_type == 'image':
            filename = '_'.join([self.tables_to_analyse.name, str(dt.datetime.now()), '.png'])
            self.analysis.savefig(os.path.join(path, filename), format='png')
