import pandas as pd


EXPORT_TYPE = '.csv'


def calculate_category_totals(table, categories, start_date, end_date, positive_expenses=True):
    """ Calculate the total flow of money in a table for a set of categories between two dates.

    :param finances_automation.entities.Table table:
    :param dict(str, list) categories:
    :param datetime.datetime start_date:
    :param datetime.datetime end_date:
    :param bool positive_expenses:
    :return pd.DataFrame:
    """
    totals = pd.DataFrame(columns=('start_date', 'end_date', categories))

    all_categories = categories['income'] + categories['expense']

    for category in all_categories:
        conditions = (
            (table.data['category'] == category)
            & (table.data[table.date_columns[0]] >= start_date)
            & (table.data[table.date_columns[0]] <= end_date)
        )

        category_total = (
            table.data[conditions][table.monetary_columns[0]].sum()
            - table.data[conditions][table.monetary_columns[1]].sum()
        )

        if positive_expenses:
            if category in categories['expense']:
                category_total = - category_total

        totals.loc[0, category] = round(category_total, 2)

    return totals
