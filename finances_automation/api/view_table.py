import sys

import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


MAX_ROWS = 500
TABLE = Table.get_table(sys.argv[1].upper())
COLUMNS = sys.argv[2:] or list(TABLE.schema.keys())

pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 500)
pd.set_option('max_colwidth', 40)
pd.set_option('display.width', 1000)


def view_table():
    """ View a table from the database.
    """
    db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    data = db.select_from(table=TABLE, columns=COLUMNS)
    dataframe = pd.DataFrame(data=data, columns=COLUMNS)
    print(dataframe.to_string(index=False))


if __name__ == '__main__':
    view_table()
