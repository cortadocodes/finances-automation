import os
import sys

from finances_automation.entities.table import Table
from finances_automation.operations.parse import CSVCleaner


def parse_statement(statement_location, table):
    """ Read in a statement, clean it up and store it in the database.

    :param str statement_location:
    :param Table table:
    """
    parser = CSVCleaner(table, statement_location)
    parser.parse()


if __name__ == '__main__':
    statement_location = os.path.abspath(sys.argv[1])
    table = Table.get_table(sys.argv[2])
    parse_statement(statement_location, table)
