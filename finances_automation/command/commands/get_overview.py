import datetime as dt

from finances_automation.entities.table import Table
from finances_automation.repositories import TransactionsRepository


def get_overview(cli_args):
    """ Send an overview of transactions to the command line.

    :param tuple cli_args:
    :return None:
    """
    table_names = 'current_transactions', 'credit_transactions'
    print_last_recorded_balance(table_names)
    print_dates_of_most_recent_data(table_names)


def print_last_recorded_balance(table_names):
    """ Print the latest recorded balance of the given tables.

    :param list(str) table_names:
    :return None:
    """
    for table_name in table_names:
        repository = TransactionsRepository(Table.get_from_config(table_name))
        latest_balance = repository.get_latest_balance()
        print('Latest balance for {}: {}'.format(table_name, float(latest_balance[0])))

    print()


def print_dates_of_most_recent_data(table_names):
    """ Print the dates of the most recently parsed and most recently categorised transactions for the given tables.

    :param list(str) table_names:
    :return:
    """
    repositories = [TransactionsRepository(Table.get_from_config(table_name)) for table_name in table_names]

    latest_parsed_dates = [repository.get_latest_parsed_transaction_date() for repository in repositories]
    latest_categorised_dates = [repository.get_latest_categorised_transaction_date() for repository in repositories]

    for table_name, latest_parsed_date, latest_categorised_date in zip(
        table_names,
        latest_parsed_dates,
        latest_categorised_dates
    ):
        print(
            'Most recent {} data:'
            '\n- Parsed: {}'
            '\n- Categorised: {}'
            .format(
                table_name,
                dt.datetime.strftime(latest_parsed_date[0], '%d/%m/%Y'),
                dt.datetime.strftime(latest_categorised_date[0], '%d/%m/%Y')
            ),
            end='\n\n'
        )
