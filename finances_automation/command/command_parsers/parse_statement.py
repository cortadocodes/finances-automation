from finances_automation import configuration as conf


def set_up_parse(subparsers):
    parse = subparsers.add_parser('parse', help='Parse a UTF-8 .csv financial statement.')

    parse.add_argument(
        'file', help='Path of file to parse.'
    )
    parse.add_argument(
        'table_name',
        choices=conf.transaction_table_names,
        help='Name of table to store parsed statement in.'
    )

    return subparsers, parse
