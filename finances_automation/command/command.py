import argparse

from finances_automation.command import command_parsers


main_parser = argparse.ArgumentParser(prog='finances-automation', description='Automate your finances analysis.')
subparsers = main_parser.add_subparsers(title='Subcommands')

subparsers, parse_statement = command_parsers.set_up_parse(subparsers)
subparsers, categorise = command_parsers.set_up_categorise(subparsers)
subparsers, analyse = command_parsers.set_up_analyse(subparsers)
subparsers, view_latest = command_parsers.set_up_view_latest(subparsers)

cli_args = main_parser.parse_args()

# Only import command functions if functionality is requested; this keeps the CLI's response quick for help requests.
from finances_automation.command import commands

main_parser.set_defaults(func=commands.get_overview)
parse_statement.set_defaults(func=commands.parse_statement)
categorise.set_defaults(func=commands.categorise_transactions)
analyse.set_defaults(func=commands.analyse_transactions)
view_latest.set_defaults(func=commands.view_latest)

# Get the arguments again to allow access to the newly-imported functions.
cli_args = main_parser.parse_args()

cli_args.func(cli_args)
