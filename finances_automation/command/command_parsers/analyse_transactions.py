from finances_automation import configuration as conf
from finances_automation.operations.analyses import get_available_analyses


def set_up_analyse(subparsers):
    analyse = subparsers.add_parser('analyse', help='Analyse transactions from a transactions table.')

    analyse.add_argument(
        'analysis_type',
        choices=get_available_analyses().keys(),
        help='Name of analysis to carry out.'
    )
    analyse.add_argument(
        'table_to_analyse',
        choices=conf.analysis_table_names,
        help='Name of table containing transactions to analyse.'
    )
    analyse.add_argument(
        'start_date',
        help='Start the analysis from this date (inclusive).'
    )
    analyse.add_argument(
        'end_date',
        help='End the analysis at this date (inclusive).'
    )
    analyse.add_argument(
        '-s',
        '--table_to_store',
        help='Name of table to store the analysis in.'
    )
    analyse.add_argument(
        '-e',
        '--export',
        action='store_true',
        help='Export the analysis to the default directory.'
    )

    return subparsers, analyse
