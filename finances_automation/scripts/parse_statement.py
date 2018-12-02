import os
import sys

from finances_automation.scripts import configuration as conf
from finances_automation.parsers import CSVCleaner


STATEMENT_LOCATION = os.path.abspath(sys.argv[1])
TYPE = sys.argv[2].lower()


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    if TYPE == 'current' or None:
        table_name = conf.TRANSACTIONS_TABLE
    elif TYPE == 'credit':
        table_name = conf.CREDIT_TRANSACTIONS_TABLE

    p = CSVCleaner(table_name, STATEMENT_LOCATION)
    p.read(header=3)
    p.clean()
    p.store_in_database()


if __name__ == '__main__':
    parse_statement()
