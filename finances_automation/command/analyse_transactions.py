import os

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.operations.analyse import Analyser


OUTPUT_PATH = os.path.join(conf.package_root, 'data')


def analyse_transactions(cli_args):
    """ Analyse transactions stored in a given database table between the given dates.

    :param str analysis_type:
    :param list(Table) table_to_analyse:
    :param Table table_to_store:
    :param str start_date:
    :param str end_date:
    """
    analysis_type = cli_args.analysis_type.lower()
    table_to_analyse = Table.get_from_config(cli_args.table_to_analyse_name)
    start_date = cli_args.start_date
    end_date = cli_args.end_date
    table_to_store = cli_args.table_to_store_name

    if table_to_store:
        table_to_store = Table.get_from_config(table_to_store)

    analyser = Analyser(analysis_type, table_to_analyse, start_date, end_date, table_to_store)
    analyser.analyse()
    analyser.export(OUTPUT_PATH)
