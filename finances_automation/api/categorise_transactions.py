import sys

from finances_automation.operations.categorise import Categoriser
from finances_automation import configuration as conf
from finances_automation.entities.table import Table


TABLE_NAME = sys.argv[1].upper()
START_DATE = sys.argv[2]
END_DATE = sys.argv[3]


if hasattr(conf, TABLE_NAME):
    TABLE_CONF = getattr(conf, TABLE_NAME)
    TABLE = Table(**TABLE_CONF)
else:
    raise ValueError('No such TABLE_NAME.')


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(TABLE, START_DATE, END_DATE)
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions()
