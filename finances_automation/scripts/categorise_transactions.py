import sys

from finances_automation.categorise import Categoriser


START_DATE = sys.argv[1]
END_DATE = sys.argv[2]


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(START_DATE, END_DATE)
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions()
