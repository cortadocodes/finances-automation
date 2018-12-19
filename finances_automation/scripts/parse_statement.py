import os
import sys

from finances_automation.scripts import configuration as conf
from finances_automation.operations.parsers import CSVCleaner
from finances_automation.table import Table


STATEMENT_LOCATION = os.path.abspath(sys.argv[1])
TYPE = sys.argv[2].lower()


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    if TYPE == 'current' or None:
        table = Table(conf.CURRENT_TRANSACTIONS_TABLE)
    elif TYPE == 'credit':
        table = Table(conf.CREDIT_TRANSACTIONS_TABLE)
    else:
        raise ValueError("TYPE should be 'current' or 'credit'")

    p = CSVCleaner(table, STATEMENT_LOCATION)
    p.read(header=3)
    p.clean()
    p.store_in_database()


if __name__ == '__main__':
    parse_statement()
