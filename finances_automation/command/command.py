import argparse

from finances_automation import __DESCRIPTION__
from finances_automation.command import command_parsers


def start():
    """ Start the package's command line interface.

    :return None:
    """
    main_parser = argparse.ArgumentParser(prog='finances-automation', description=__DESCRIPTION__)
    subparsers = main_parser.add_subparsers(title='Subcommands')

    subparsers, parse_statement = command_parsers.set_up_parse(subparsers)
    subparsers, categorise = command_parsers.set_up_categorise(subparsers)
    subparsers, analyse = command_parsers.set_up_analyse(subparsers)
    subparsers, view_latest = command_parsers.set_up_view_latest(subparsers)

    # Exit here after if help option is selected (after printing help message).
    main_parser.parse_args()

    # Only import command functions if functionality is requested; this keeps CLI response quick for help requests.
    from finances_automation.command import commands

    parser_functions = {
        main_parser: commands.get_overview,
        parse_statement: commands.parse_statement,
        categorise: commands.categorise_transactions,
        analyse: commands.analyse_transactions,
        view_latest: commands.view_latest
    }

    for parser, parser_function in parser_functions.items():
        parser.set_defaults(func=parser_function)

    # Get the arguments again to allow access to the newly-imported functions.
    cli_args = main_parser.parse_args()

    cli_args.func(cli_args)


if __name__ == '__main__':
    start()
