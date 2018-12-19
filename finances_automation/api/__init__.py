from finances_automation import configuration as conf
from finances_automation.entities.table import Table


def get_table(table_name):
    """ Get a Table object for table_name if its configuration exists in the configuration file.

    :param str table_name: possible name of a table

    :raise ValueError: if the a configuration doesn't exist for the table name
    :return Table: table with the table name
    """
    if hasattr(conf, table_name):
        table_conf = getattr(conf, table_name)
        return Table(**table_conf)

    raise ValueError('No such table: {}.'.format(table_name))
