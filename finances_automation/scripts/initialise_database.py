from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database()
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()
    database.create_table(conf.TRANSACTIONS_TABLE['name'], conf.TRANSACTIONS_TABLE['headers'])
    database.stop()

if __name__ == '__main__':
    initialise_database()
