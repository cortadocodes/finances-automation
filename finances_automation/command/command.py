import argparse


parser = argparse.ArgumentParser(
    prog='finances-automation',
    description='Automate finance analysis.'
)

subparsers = parser.add_subparsers(title='Subcommands')

parse_statement = subparsers.add_parser(
    'parse',
    help='Parse a UTF-8 csv financial statement.'
)

categorise = subparsers.add_parser(
    'categorise',
    help='Categorise transactions in a transactions table.'
)

analyse = subparsers.add_parser(
    'analyse',
    help='Analyse transactions in a transactions table.'
)

parser.parse_args()
