import sys

from finances_automation.operations.categorise import Categoriser
from finances_automation.api import get_table


TABLE = get_table(sys.argv[1].upper())
START_DATE = sys.argv[2]
END_DATE = sys.argv[3]


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(TABLE, START_DATE, END_DATE)
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions()
