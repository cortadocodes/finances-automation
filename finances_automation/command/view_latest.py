import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


MAX_ROWS = 500
pd.set_option('display.max_rows', MAX_ROWS)
pd.set_option('display.max_columns', 500)
pd.set_option('max_colwidth', 40)
pd.set_option('display.width', 1000)


def view_latest(cli_args):
    """ View the latest data from the specified columns of a table from the database.

    :param Table table:
    :param list(str) columns:
    """
    table = Table.get_from_config(cli_args.table_name)
    columns = cli_args.columns or list(table.schema.keys())
    limit = cli_args.n

    db = Database(conf.db_name, conf.db_cluster, conf.user)

    if columns == ['*']:
        columns = db.get_table_column_names(table)
        columns.remove('id')

    data = db.select_from(table, columns)

    df = pd.DataFrame(data=data, columns=columns).sort_values(by=table.date_columns[0], ascending=False).head(limit)

    print('\n')
    print(df.to_string(index=False))
