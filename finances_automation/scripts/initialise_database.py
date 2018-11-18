from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False

CREATE_TABLE = (
    """CREATE TABLE {} ({});"""
    .format(conf.DB_NAME, '{} ' * len(conf.TABLE_HEADERS))
    .format(*[header + ' {},\n' for header in conf.TABLE_HEADERS.keys()])
    .format(*[variable_type for variable_type in conf.TABLE_HEADERS.values()])
)


def initialise_database(db_name, db_cluster, user, table_creation_query, require_overwrite):
    """ Create and initialise a database with an empty table.
    """
    database = Database(db_name, db_cluster, user)
    database.create(overwrite=require_overwrite)
    database.start()
    database.execute_statement(table_creation_query)
    database.stop()


if __name__ == '__main__':
    initialise_database(
        conf.DB_NAME,
        conf.DB_CLUSTER,
        conf.USER,
        CREATE_TABLE,
        REQUIRE_OVERWRITE
    )
