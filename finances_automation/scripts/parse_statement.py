import sys

from finances_automation.parsers import CSVCleaner
from finances_automation.scripts import configuration as conf


STATEMENT_LOCATION = sys.argv[1]


def parse_statement():
    """ Read in a statement, clean it up and store it in the database.
    """
    p = CSVCleaner(conf.DB_NAME, conf.DB_CLUSTER, conf.USER, conf.TRANSACTIONS_TABLE['name'], STATEMENT_LOCATION)
    p.read(header=3)
    p.clean(conf.TRANSACTIONS_TABLE['monetary_columns'], conf.TRANSACTIONS_TABLE['date_column'])
    p.store_in_database()


if __name__ == '__main__':
    parse_statement()
