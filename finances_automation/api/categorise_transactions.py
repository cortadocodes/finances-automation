import sys

from finances_automation.entities.table import Table
from finances_automation.operations.categorise import Categoriser


TABLE = Table.get_table(sys.argv[1])
START_DATE = sys.argv[2]
END_DATE = sys.argv[3]


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(TABLE, START_DATE, END_DATE)
    categoriser.load()
    categoriser.select_categories()
    categoriser.store()


if __name__ == '__main__':
    categorise_transactions()
