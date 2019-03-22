from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


def initialise_database(overwrite=False):
    """ Create and initialise the database with an empty table.

    :param bool overwrite: True if existing database should be overwritten
    """
    database = Database(**conf.db_config)
    database.create(overwrite=overwrite)

    for table_name in conf.table_names:
        database.create_table(Table.get_from_config(table_name))


if __name__ == '__main__':
    initialise_database()
