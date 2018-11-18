import os
import sys

from finances_automation.parsers import Parser


STATEMENT_LOCATION = sys.argv[1]

PACKAGE_ROOT = os.path.abspath('..')
USER = 'Marcus1'

DB_NAME = 'finances'
DB_LOCATION = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')

TABLE_NAME = 'transactions'

MONETARY_COLUMNS = ['money_in', 'money_out', 'balance']
DATE_COLUMN = 'date'


def parse_statement(db_name,
                    db_location,
                    db_table,
                    user,
                    statement_location,
                    monetary_columns,
                    date_column):
    p = Parser(db_name, db_location, user, statement_location)
    p.read(header=3)
    p.clean(monetary_columns, date_column)
    p.store_in_database(db_table)


if __name__ == '__main__':
    parse_statement(
        DB_NAME,
        DB_LOCATION,
        TABLE_NAME,
        USER,
        STATEMENT_LOCATION,
        MONETARY_COLUMNS,
        DATE_COLUMN
    )
