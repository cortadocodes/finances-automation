import os
import sys

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.operations.analyse import Analyser


EXCLUDED_FROM_STORAGE = Analyser.analyses_excluded_from_storage
OUTPUT_PATH = os.path.join(conf.package_root, 'data')


def analyse_transactions(analysis_type, tables_to_analyse, table_to_store, start_date, end_date):
    """ Analyse transactions stored in a given database table between the given dates.

    :param str analysis_type:
    :param list(Table) tables_to_analyse:
    :param Table table_to_store:
    :param str start_date:
    :param str end_date:
    """
    analyser = Analyser(tables_to_analyse, table_to_store, analysis_type, start_date, end_date)
    analyser.analyse()
    analyser.export_analysis(OUTPUT_PATH)


if __name__ == '__main__':
    analysis_type = sys.argv[1].lower()
    tables_to_analyse = [Table.get_table(table_name) for table_name in sys.argv[2].split(';')]
    start_date = sys.argv[3]
    end_date = sys.argv[4]

    if analysis_type in EXCLUDED_FROM_STORAGE:
        table_to_store = None
    else:
        table_to_store = Table.get_table(analysis_type)

    analyse_transactions(analysis_type, tables_to_analyse, table_to_store, start_date, end_date)
