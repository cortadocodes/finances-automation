import sys

from finances_automation.parsers import Parser
from finances_automation.scripts import configuration as conf


STATEMENT_LOCATION = sys.argv[1]


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    p = Parser(conf.DB_NAME, conf.DB_CLUSTER, conf.USER, conf.TABLE_NAME, STATEMENT_LOCATION)
    p.read(header=3)
    p.clean(conf.MONETARY_COLUMNS, conf.DATE_COLUMN)
    p.store_in_database()


if __name__ == '__main__':
    parse_statement()
