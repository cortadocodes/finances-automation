def table_validator(func):
    def table_validator(self, name, type, schema, monetary_columns=None, date_columns=None, date_format=None,
                        category_columns=None):
        """ Check if Table initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(name, str):
            raise TypeError('name should be a string.')
        if not isinstance(type, str):
            raise TypeError('type should be a string')
        if not isinstance(schema, dict):
            raise TypeError('schema should be a dictionary.')
        if monetary_columns and not isinstance(monetary_columns, list):
            raise TypeError('monetary_columns should be a list of strings.')
        if date_columns and not isinstance(date_columns, list):
            raise TypeError('date_columns should be a list of strings.')
        if date_format and not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')
        if category_columns and not isinstance(category_columns, list):
            raise TypeError('category_columns should be a list of strings.')

        return func(self, name, type, schema, monetary_columns, date_columns, date_format, category_columns)

    return table_validator
