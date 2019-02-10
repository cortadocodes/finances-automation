def table_validator(func):
    def table_validator(self, name, type_, schema, monetary_columns=None, date_columns=None, date_format=None,
                        category_columns=None):
        """ Check if Table initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        types = {
            'name': str,
            'type_': str,
            'schema': dict,
            'monetary_columns': list,
            'date_columns': list,
            'date_format': str,
            'category_columns': list
        }
        error_message = '{} parameter should be of type {}; received {}.'

        if not isinstance(name, str):
            raise TypeError(error_message.format('name', types['name'], name))
        if not isinstance(type_, str):
            raise TypeError(error_message.format('type_', types['type_'], type_))
        if not isinstance(schema, dict):
            raise TypeError(error_message.format('schema', types['schema'], schema))
        if monetary_columns and not isinstance(monetary_columns, list):
            raise TypeError(error_message.format('monetary_columns', types['monetary_columns'], monetary_columns))
        if date_columns and not isinstance(date_columns, list):
            raise TypeError(error_message.format('date_columns', types['date_columns'], date_columns))
        if date_format and not isinstance(date_format, str):
            raise TypeError(error_message.format('date_format', types['date_format'], date_format))
        if category_columns and not isinstance(category_columns, list):
            raise TypeError(error_message.format('category_columns', types['category_columns'], category_columns))

        return func(self, name, type_, schema, monetary_columns, date_columns, date_format, category_columns)

    return table_validator
