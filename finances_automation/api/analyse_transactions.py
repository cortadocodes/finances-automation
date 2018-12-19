import sys

from finances_automation.operations.analyse import Analyser
from finances_automation import configuration as conf
from finances_automation.entities.table import Table


TABLES = (sys.argv[1].upper(), sys.argv[2].upper())
START_DATE = sys.argv[3]
END_DATE = sys.argv[4]


for table in TABLES:
    if hasattr(conf, table):
        TABLE_CONF = getattr(conf, table)
        TABLE = Table(**TABLE_CONF)
    else:
        raise ValueError('No such table: [{}].'.format(table))


def analyse_transactions():
    analyser = Analyser(TABLE, START_DATE, END_DATE)
    analyser.load_from_database()
    analyser.calculate_totals()
    analyser.store_in_database()


if __name__ == '__main__':
    analyse_transactions()
