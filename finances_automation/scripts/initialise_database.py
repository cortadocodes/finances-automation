from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False

CREATE_TABLE = (
    """CREATE TABLE {} ({});"""
    .format(conf.DB_NAME, '{} ' * len(conf.TABLE_HEADERS))
    .format(*[header + ' {},\n' for header in conf.TABLE_HEADERS.keys()])
    .format(*[variable_type for variable_type in conf.TABLE_HEADERS.values()])
)


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()
    database.execute_statement(CREATE_TABLE)
    database.stop()


if __name__ == '__main__':
    initialise_database()
