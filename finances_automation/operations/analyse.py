import datetime as dt
import os

from finances_automation import configuration as conf
from finances_automation.operations import analyses
from finances_automation.repositories import BaseRepository
from finances_automation.validation.analyse import analyser_validator


class Analyser:

    @analyser_validator
    def __init__(self, analysis_type, table_to_analyse, start_date, end_date, table_to_store=None):
        """ Initialise an Analyser.

        :param str analysis_type: name of analysis_result to carry out
        :param finances_automation.entities.table.Table table_to_analyse: table to analyse
        :param finances_automation.entities.table.Table table_to_store: table to store analysis_result in
        :param str start_date: date to start analysis_result at
        :param str end_date: date to end analysis_result at
        """
        self.available_analyses = analyses.get_available_analyses()
        self.chosen_analysis = analyses.get_analysis(analysis_type)

        self.analysis_result = None
        self.categories = conf.categories

        self.table_to_analyse = table_to_analyse
        self.table_to_store = table_to_store

        self.repositories = {'table_to_analyse': BaseRepository(self.table_to_analyse)}

        if self.table_to_store:
            self.repositories['table_to_store'] = BaseRepository(self.table_to_store)

        self.start_date, self.end_date = (
            dt.datetime.strptime(date, self.table_to_analyse.date_format).date()
            for date in (start_date, end_date)
        )

    def analyse(self):
        """Perform an analysis on a table between two dates, storing it in the database.

        :return None:
        """
        self.repositories['table_to_analyse'].load(self.start_date, self.end_date)

        self.analysis_result = self.chosen_analysis(
            table=self.table_to_analyse,
            categories=self.categories,
            start_date=self.start_date,
            end_date=self.end_date,
            show_plot=True
        )

        self._store()

    def _store(self):
        """ Store the analysis result in the database.

        :return None:
        """
        if self.chosen_analysis.__name__ not in analyses.ANALYSES_EXCLUDED_FROM_STORAGE:
            self._set_metadata()
            self.repositories['table_to_store'].insert(self.analysis_result)

    def _set_metadata(self):
        """ Add analysis metadata to the database entry.

        :return None:
        """
        self.analysis_result['tables_analysed'] = self.table_to_analyse.name
        self.analysis_result['start_date'] = self.start_date
        self.analysis_result['end_date'] = self.end_date
        self.analysis_result['analysis_datetime'] = dt.datetime.now()

    def export(self, path):
        """ Export the analysis to a local location.

        :param str path:
        :return None:
        """
        export_type = analyses.ANALYSIS_NAMES_AND_EXPORT_TYPES[self.chosen_analysis.__name__]

        if self.analysis_result is None:
            raise ValueError('No analysis to be exported.')

        if not os.path.exists(path):
            os.makedirs(path)

        filename = self.table_to_analyse.name + '_' + str(self.analysis_result['analysis_datetime']) + export_type

        if export_type == '.csv':
            self.analysis_result.to_csv(os.path.join(path, filename), index=False, encoding='utf-8')
        elif export_type == '.png':
            self.analysis_result.savefig(os.path.join(path, filename), format='png')
