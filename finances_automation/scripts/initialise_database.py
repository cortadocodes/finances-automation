from finances_automation.database import Database
from finances_automation.scripts import configuration as conf
from finances_automation.table import Table


REQUIRE_OVERWRITE = False


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()

    tables = [
        Table(**config) for config in
        (
            conf.CURRENT_TRANSACTIONS_TABLE,
            conf.CREDIT_TRANSACTIONS_TABLE,
            conf.MONTHLY_TOTALS_TABLE
        )
    ]

    yield (database.create_table(table) for table in tables)

    database.stop()

if __name__ == '__main__':
    initialise_database()
