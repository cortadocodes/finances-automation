from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


REQUIRE_OVERWRITE = False


def initialise_database():
    """ Create and initialise the database with an empty table.
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=REQUIRE_OVERWRITE)

    table_names = 'CURRENT_TRANSACTIONS_TABLE', 'CREDIT_TRANSACTIONS_TABLE', 'TOTALS_TABLE'

    for table_name in table_names:
        database.create_table(Table.get_table(table_name))


if __name__ == '__main__':
    initialise_database()
