import itertools

from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False

transactions_schema_list = list(
    itertools.chain(*zip(conf.TRANSACTIONS_TABLE['headers'].keys(), conf.TRANSACTIONS_TABLE['headers'].values()))
)

transactions_schema = ',\n'.join(
    ['{} {}' for header in conf.TRANSACTIONS_TABLE['headers']]
).format(*transactions_schema_list)

CREATE_TABLE = (
    """
    CREATE TABLE {} (
        {}
    );
    """
    .format(conf.TRANSACTIONS_TABLE['name'], transactions_schema)
)


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database()
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()
    database.execute_statement(CREATE_TABLE)
    database.stop()


if __name__ == '__main__':
    initialise_database()
