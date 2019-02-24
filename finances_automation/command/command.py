import argparse

from finances_automation.command import command_parsers


parser = argparse.ArgumentParser(prog='finances-automation', description='Automate finance analysis.')
subparsers = parser.add_subparsers(title='Subcommands')

subparsers, parse_statement = command_parsers.parse_statement(subparsers)
subparsers, categorise = command_parsers.categorise_transactions(subparsers)
subparsers, analyse = command_parsers.analyse_transactions(subparsers)
subparsers, view_latest = command_parsers.view_latest(subparsers)

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
