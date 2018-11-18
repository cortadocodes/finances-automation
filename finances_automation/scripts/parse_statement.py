import sys

from finances_automation.parsers import Parser
from finances_automation.scripts import configuration as conf


STATEMENT_LOCATION = sys.argv[1]


def parse_statement():
    p = Parser(conf.DB_NAME, conf.DB_CLUSTER, conf.USER, STATEMENT_LOCATION)
    p.read(header=3)
    p.clean(conf.MONETARY_COLUMNS, conf.DATE_COLUMN)
    p.store_in_database(conf.TABLE_NAME)


if __name__ == '__main__':
    parse_statement()
