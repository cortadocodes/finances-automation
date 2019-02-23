import os
import sys

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.operations.analyse import Analyser


OUTPUT_PATH = os.path.join(conf.package_root, 'data')


def analyse_transactions(analysis_type, table_to_analyse, start_date, end_date, table_to_store=None):
    """ Analyse transactions stored in a given database table between the given dates.

    :param str analysis_type:
    :param list(Table) table_to_analyse:
    :param Table table_to_store:
    :param str start_date:
    :param str end_date:
    """
    analyser = Analyser(analysis_type, table_to_analyse, start_date, end_date, table_to_store)
    analyser.analyse()
    analyser.export(OUTPUT_PATH)


if __name__ == '__main__':
    analysis_type = sys.argv[1].lower()
    table_to_analyse = Table.get_from_config(sys.argv[2].lower())
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    table_to_store = sys.argv[5]

    if table_to_store:
        table_to_store = Table.get_from_config(analysis_type)

    analyse_transactions(analysis_type, table_to_analyse, start_date, end_date, table_to_store)
