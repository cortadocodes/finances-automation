import sys

import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


MAX_ROWS = 500
pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 500)
pd.set_option('max_colwidth', 40)
pd.set_option('display.width', 1000)


def view_table(table, columns):
    """ View a table from the database.

    :param Table table:
    :param list(str) columns:
    """
    db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    data = db.select_from(table, columns)
    if columns == ['*']:
        columns = db.get_table_column_names(table)
    dataframe = pd.DataFrame(data=data, columns=columns)
    return dataframe


if __name__ == '__main__':
    table = Table.get_table(sys.argv[1])
    columns = sys.argv[2:] or list(table.schema.keys())
    df = view_table(table, columns)
    print(df.to_string(index=False))
