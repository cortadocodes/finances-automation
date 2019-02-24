import argparse


parser = argparse.ArgumentParser(prog='finances-automation', description='Automate finance analysis.')
subparsers = parser.add_subparsers(title='Subcommands')

parse_statement = subparsers.add_parser('parse', help='Parse a UTF-8 csv financial statement.')
parse_statement.add_argument('file', help='Path of file to parse.')
parse_statement.add_argument('table_name', help='Name of table to store parsed statement in.')

categorise = subparsers.add_parser('categorise', help='Categorise transactions from a transactions table.')
categorise.add_argument('table_name', help='Name of table containing transactions to categorise.')
categorise.add_argument('start_date', help='Start the categorisation from this date (inclusive).')
categorise.add_argument('end_date', help='End the categorisation at this date (inclusive).')

analyse = subparsers.add_parser('analyse', help='Analyse transactions from a transactions table.')
analyse.add_argument('analysis_type', help='Name of analysis to carry out.')
analyse.add_argument('table_to_analyse', help='Name of table containing transactions to analyse.')
analyse.add_argument('start_date', help='Start the analysis from this date (inclusive).')
analyse.add_argument('end_date', help='End the analysis at this date (inclusive).')
analyse.add_argument('-s', '--table_to_store', help='Name of table to store the analysis in.')
analyse.add_argument('-e', '--export', action='store_true', help='Export the analysis to the default directory.')

view_latest = subparsers.add_parser('view_latest', help='View the latest n transactions from a table.')
view_latest.add_argument('table_name', help='Name of table to view.')
view_latest.add_argument('-n', type=int, default=50, help='Number of transactions to view.')
view_latest.add_argument('-c', '--columns', default=['*'], help='List of columns to view.')

cli_args = parser.parse_args()

# Only import command functions if functionality is requested; this keeps the CLI's response quick for help requests.
from finances_automation import command

parser.set_defaults(func=command.get_overview)
parse_statement.set_defaults(func=command.parse_statement)
categorise.set_defaults(func=command.categorise_transactions)
analyse.set_defaults(func=command.analyse_transactions)
view_latest.set_defaults(func=command.view_latest)

# Get the arguments again to allow access to the newly-imported functions.
cli_args = parser.parse_args()

cli_args.func(cli_args)
