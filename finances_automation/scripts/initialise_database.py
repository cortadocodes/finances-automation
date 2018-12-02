from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()

    database.create_table(
        conf.TRANSACTIONS_TABLE['name'], conf.TRANSACTIONS_TABLE['headers']
    )
    database.create_table(
        conf.CREDIT_TRANSACTIONS_TABLE['name'], conf.CREDIT_TRANSACTIONS_TABLE['headers']
    )
    database.create_table(
        conf.MONTHLY_TOTALS_TABLE['name'], conf.MONTHLY_TOTALS_TABLE['headers']
    )

    database.stop()

if __name__ == '__main__':
    initialise_database()
