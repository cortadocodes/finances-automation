import logging

from finances_automation import configuration as conf
from finances_automation.entities.table import Table
from finances_automation.repositories import BaseRepository


logger = logging.getLogger(__name__)


def initialise_database():
    """ Create and initialise the database with all tables in the configuration file.

    :return None:
    """
    for table_name in conf.table_names:
        BaseRepository(Table.get_from_config(table_name)).create_table()
        logger.info('Created table %r', table_name)


if __name__ == '__main__':
    initialise_database()
