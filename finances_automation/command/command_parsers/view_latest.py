from finances_automation import configuration as conf


def set_up_view_latest(subparsers):
    view_latest = subparsers.add_parser('view_latest', help='View the latest entries to a table.')

    view_latest.add_argument(
        'table_name',
        choices=conf.table_names,
        help='Name of table to view.'
    )
    view_latest.add_argument(
        '-n',
        type=int,
        default=50,
        help='Number of transactions to view.'
    )
    view_latest.add_argument(
        '-c',
        '--columns',
        default=['*'],
        nargs='*',
        help='List of columns to view.'
    )

    return subparsers, view_latest
