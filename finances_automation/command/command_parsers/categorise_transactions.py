from finances_automation import configuration as conf


def set_up_categorise(subparsers):
    categorise = subparsers.add_parser('categorise', help='Categorise transactions from a transactions table.')

    categorise.add_argument(
        'table_name',
        choices=conf.transaction_table_names,
        help='Name of table containing transactions to categorise.'
    )
    categorise.add_argument(
        'start_date',
        help='Start the categorisation from this date (inclusive).'
    )
    categorise.add_argument(
        'end_date',
        help='End the categorisation at this date (inclusive).'
    )

    return subparsers, categorise
