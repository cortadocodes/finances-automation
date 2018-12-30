from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


def initialise_database(overwrite):
    """ Create and initialise the database with an empty table.

    :param bool overwrite: True if existing database should be overwritten
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=overwrite)

    table_names = 'current_transactions', 'credit_transactions', 'totals', 'monthly_averages'

    for table_name in table_names:
        database.create_table(Table.get_table(table_name))


if __name__ == '__main__':
    require_overwrite = False
    initialise_database(require_overwrite)
