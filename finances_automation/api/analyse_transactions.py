import os
import sys

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.operations.analyse import Analyser


EXCLUDED = Analyser.analyses_excluded_from_storage

ANALYSIS_TYPE = sys.argv[1].lower()

TABLE_TO_ANALYSE = Table.get_table(sys.argv[2])

START_DATE = sys.argv[3]
END_DATE = sys.argv[4]

if ANALYSIS_TYPE in EXCLUDED:
    TABLE_TO_STORE = None
else:
    TABLE_TO_STORE = Table.get_table(ANALYSIS_TYPE)

OUTPUT_CSV_PATH = os.path.join(conf.PACKAGE_ROOT, 'data')


def analyse_transactions():
    """ Analyse transactions stored in a given database table between the given dates.
    """
    analyser = Analyser(TABLE_TO_ANALYSE, TABLE_TO_STORE, ANALYSIS_TYPE, START_DATE, END_DATE)
    analyser.analyse()

    if ANALYSIS_TYPE not in EXCLUDED:
        analyser.get_analysis_as_csv(OUTPUT_CSV_PATH)


if __name__ == '__main__':
    analyse_transactions()
