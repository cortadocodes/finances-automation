from finances_automation.entities.table import Table
from finances_automation.operations.categorise import Categoriser


def categorise_transactions(cli_args):
    """ Load transactions from the database, categorise them, and update the database with these categories.

    :param Table table:
    :param str start_date:
    :param str end_date:
    """
    table = Table.get_from_config(cli_args.table_name)
    start_date = cli_args.start_date
    end_date = cli_args.end_date

    categoriser = Categoriser(table, start_date, end_date)
    categoriser.select_categories()
