from finances_automation.operations import analyses


def test_get_available_analyses():
    """ Test all expected analyses are available.

    :raise AssertionError:
    :return None:
    """
    expected_output = {
        'calculate_category_totals': analyses.calculate_category_totals,
        'plot_balance': analyses.plot_balance
    }

    assert analyses.get_available_analyses() == expected_output
