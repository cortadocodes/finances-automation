import os
import sys

from finances_automation.parsers import CSVCleaner


STATEMENT_LOCATION = os.path.abspath(sys.argv[1])


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    p = CSVCleaner(STATEMENT_LOCATION)
    p.read(header=3)
    p.clean()
    p.store_in_database()


if __name__ == '__main__':
    parse_statement()
