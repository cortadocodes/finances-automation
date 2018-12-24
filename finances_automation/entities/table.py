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
