import sys

from finances_automation.parsers import Parser
from finances_automation.scripts import configuration as conf


STATEMENT_LOCATION = sys.argv[1]


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
        conf.DB_NAME,
        conf.DB_CLUSTER,
        conf.TABLE_NAME,
        conf.USER,
        STATEMENT_LOCATION,
        conf.MONETARY_COLUMNS,
        conf.DATE_COLUMN
    )
