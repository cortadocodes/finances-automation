from finances_automation.entities.database import Database
from finances_automation import configuration as conf
from finances_automation.entities.table import Table


REQUIRE_OVERWRITE = False


def initialise_database():
    """ Create and initialise the database with an empty table.
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

    for table in tables:
        database.create_table(table)

    database.stop()

if __name__ == '__main__':
    initialise_database()
