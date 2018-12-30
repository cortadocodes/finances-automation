import sys

from finances_automation.entities.table import Table
from finances_automation.operations.categorise import Categoriser


def categorise_transactions(table, start_date, end_date):
    """ Load transactions from the database, categorise them, and update the database with these categories.

    :param Table table:
    :param str start_date:
    :param str end_date:
    """
    categoriser = Categoriser(table, start_date, end_date)
    categoriser.load()
    categoriser.select_categories()
    categoriser.store()


if __name__ == '__main__':
    table = Table.get_table(sys.argv[1])
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    categorise_transactions(table, start_date, end_date)
