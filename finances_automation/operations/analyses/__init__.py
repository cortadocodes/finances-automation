import sys

from . import calculate_category_totals
from . import calculate_category_averages
from . import calculate_category_totals_across_accounts
from . import plot_balance


THIS_MODULE = sys.modules[__name__]


def get_available_analyses():
    analysis_names = {
        'calculate_category_totals',
        'calculate_category_averages',
        'calculate_category_totals_across_accounts',
        'plot_balance'
    }

    return {
        analysis_name: getattr(THIS_MODULE, analysis_name)
        for analysis_name in analysis_names
    }
