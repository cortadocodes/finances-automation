import os

from finances_automation.entities.table import Table
from finances_automation.operations.parse import CSVParser


def parse_statement(cli_args):
    """ Read in a statement, clean it up and store it in the database.

    :param str statement_location:
    :param str table_name:
    """
    statement_location = os.path.abspath(cli_args.file)
    table_name = Table.get_from_config(cli_args.table_name)

    parser = CSVParser(table_name, statement_location)
    parser.parse()
