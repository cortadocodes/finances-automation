import sys

from finances_automation.operations.categorise import Categoriser
from finances_automation.scripts import configuration as conf
from finances_automation.entities.table import Table


table_name = sys.argv[1]
for attr in conf.__dict__:
    if hasattr(conf, table_name.upper()):
        TABLE = Table(**conf.table_name)
    else:
        raise ValueError('No such table_name.')

START_DATE = sys.argv[2]
END_DATE = sys.argv[3]


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(START_DATE, END_DATE, TABLE)
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions()
