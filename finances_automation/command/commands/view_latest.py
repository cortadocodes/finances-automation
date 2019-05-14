import pandas as pd

from finances_automation.entities.table import Table
from finances_automation.repositories import TransactionsRepository


pd.set_option('display.max_columns', 500)
pd.set_option('max_colwidth', 40)
pd.set_option('display.width', 1000)


def view_latest(cli_args):
    """ View the latest data from the specified columns of a table from the database.

    :param Table table:
    :param list(str) columns:
    """
    table = Table.get_from_config(cli_args.table_name)
    columns = cli_args.columns
    limit = cli_args.n

    if columns == ['*']:
        columns = list(table.schema.keys())
        columns.remove('id')

    elif 'date' not in columns:
        columns = ['date'] + columns

    data = TransactionsRepository(table).get_latest_entries(columns, limit)

    df = pd.DataFrame(data=data, columns=columns).sort_values(by=table.date_columns[0], ascending=False)

    print('\n')
    print(df.to_string(index=False))
