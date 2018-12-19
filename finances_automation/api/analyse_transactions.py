import sys

from finances_automation.api import get_table
from finances_automation.operations.analyse import Analyser


TABLE_TO_ANALYSE = get_table(sys.argv[1].upper())
TABLE_TO_STORE = get_table(sys.argv[2].upper())

START_DATE = sys.argv[3]
END_DATE = sys.argv[4]


def analyse_transactions():
    analyser = Analyser(TABLE_TO_ANALYSE, TABLE_TO_STORE, START_DATE, END_DATE)
    analyser.load_from_database()
    analyser.calculate_totals()
    analyser.store_in_database()


if __name__ == '__main__':
    analyse_transactions()
