from finances_automation import configuration as conf


class Table:

    def __init__(self, name, schema, monetary_columns=None, date_columns=None, date_format=None,
                 category_columns=None):

        self.name = name
        self.schema = schema
        self.monetary_columns = monetary_columns
        self.date_columns = date_columns
        self.date_format = date_format
        self.category_columns = category_columns

    @staticmethod
    def check_types(name, schema, monetary_columns, date_columns, date_format,
                    category_columns):

        if not isinstance(name, str):
            raise TypeError('name should be a string.')
        if not isinstance(schema, dict):
            raise TypeError('schema should be a dictionary.')
        if not isinstance(monetary_columns, list):
            raise TypeError('monetary_columns should be a list of strings.')
        if not isinstance(date_columns, list):
            raise TypeError('date_columns should be a list of strings.')
        if not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')
        if not isinstance(category_columns, list):
            raise TypeError('category_columns should be a list of strings.')

    @staticmethod
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
