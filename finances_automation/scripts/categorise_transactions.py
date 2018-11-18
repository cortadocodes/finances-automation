from finances_automation.categorise import Categoriser
from finances_automation.scripts import configuration as conf


def categorise_transactions(db_name,
                            db_location,
                            user,
                            income_categories,
                            expense_categories,
                            table_name,
                            table_headers):
    categoriser = Categoriser(db_name, db_location, user, income_categories, expense_categories)
    categoriser.load_from_database(table_name, table_headers)
    categoriser.select_categories()
    categoriser.store_in_database(table_name)


if __name__ == '__main__':
    categorise_transactions(
        conf.DB_NAME,
        conf.DB_CLUSTER,
        conf.USER,
        conf.INCOME_CATEGORIES,
        conf.EXPENSE_CATEGORIES,
        conf.TABLE_NAME,
        conf.TABLE_HEADERS
    )
