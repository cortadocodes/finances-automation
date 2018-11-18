import sys

from finances_automation.categorise import Categoriser
from finances_automation.scripts import configuration as conf


START_DATE = sys.argv[1]
END_DATE = sys.argv[2]


def categorise_transactions(db_name,
                            db_location,
                            db_user,
                            table_name,
                            table_headers,
                            date_column,
                            start_date,
                            end_date,
                            income_categories,
                            expense_categories,
                            category_columns):

    categoriser = Categoriser(
        db_name,
        db_location,
        db_user,
        table_name,
        table_headers,
        income_categories,
        expense_categories,
        category_columns,
        date_column,
        start_date,
        end_date
    )
    categoriser.load_from_database()
    categoriser.select_categories()
    categoriser.store_in_database()


if __name__ == '__main__':
    categorise_transactions(
        conf.DB_NAME,
        conf.DB_CLUSTER,
        conf.USER,
        conf.TABLE_NAME,
        conf.TABLE_HEADERS,
        conf.INCOME_CATEGORIES,
        conf.EXPENSE_CATEGORIES,
        conf.CATEGORY_COLUMNS,
        conf.DATE_COLUMN,
        START_DATE,
        END_DATE
    )
