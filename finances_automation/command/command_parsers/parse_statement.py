from finances_automation import configuration as conf


def parse_statement(subparsers):
    parse_statement = subparsers.add_parser('parse', help='Parse a UTF-8 csv financial statement.')
    parse_statement.add_argument('file', help='Path of file to parse.')
    parse_statement.add_argument(
        'table_name',
        choices=conf.transaction_table_names,
        help='Name of table to store parsed statement in.'
    )

    return subparsers, parse_statement