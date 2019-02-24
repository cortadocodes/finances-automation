from finances_automation import configuration as conf


def view_latest(subparsers):
    view_latest = subparsers.add_parser('view_latest', help='View the latest n transactions from a table.')
    view_latest.add_argument(
        'table_name',
        choices=conf.table_names,
        help='Name of table to view.'
    )
    view_latest.add_argument('-n', type=int, default=50, help='Number of transactions to view.')
    view_latest.add_argument('-c', '--columns', default=['*'], help='List of columns to view.')

    return subparsers, view_latest