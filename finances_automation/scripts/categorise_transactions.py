import sys

from finances_automation.categorise import Categoriser
from finances_automation.scripts import configuration as conf


START_DATE = sys.argv[1]
END_DATE = sys.argv[2]


def categorise_transactions():
    """ Load transactions from the database, categorise them, and update the database with these categories.
    """
    categoriser = Categoriser(
        conf.DB_NAME,
        conf.DB_CLUSTER,
        conf.USER,
        conf.TABLE_NAME,
        conf.TABLE_HEADERS,
        conf.INCOME_CATEGORIES,
        conf.EXPENSE_CATEGORIES,
        conf.CATEGORY_COLUMNS,
        conf.DATE_COLUMN,
        conf.DATE_FORMAT,
        START_DATE,
        END_DATE
    )
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions()
