import os
import sys

from finances_automation.entities.table import Table
from finances_automation.operations.parse import CSVCleaner


STATEMENT_LOCATION = os.path.abspath(sys.argv[1])
TABLE = Table.get_table(sys.argv[2])


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    parser = CSVCleaner(TABLE, STATEMENT_LOCATION)
    parser.read(header=3)
    parser.clean()
    parser.store()


if __name__ == '__main__':
    parse_statement()
