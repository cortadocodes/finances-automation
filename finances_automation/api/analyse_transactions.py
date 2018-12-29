import os
import sys

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.operations.analyse import Analyser


TABLE_TO_ANALYSE = Table.get_table(sys.argv[1].upper())
TABLE_TO_STORE = Table.get_table(sys.argv[2].upper())

ANALYSIS_TYPE = sys.argv[3].lower()

START_DATE = sys.argv[4]
END_DATE = sys.argv[5]

OUTPUT_CSV_PATH = os.path.join(conf.PACKAGE_ROOT, 'data')


def analyse_transactions():
    """ Analyse transactions stored in a given database table between the given dates.
    """
    analyser = Analyser(TABLE_TO_ANALYSE, TABLE_TO_STORE, ANALYSIS_TYPE, START_DATE, END_DATE)
    analyser.load()
    analyser.analyse()
    analyser.get_analysis_as_csv(OUTPUT_CSV_PATH)
    analyser.store()


if __name__ == '__main__':
    analyse_transactions()
