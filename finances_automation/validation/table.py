def table_validator(func):
    def table_validator(instance, name, type_, schema, monetary_columns=None, date_columns=None, date_format=None,
                        category_columns=None):
        """ Check if Table initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        attribute_types = {
            'name': [str],
            'type_': [str],
            'schema': [dict],
            'monetary_columns': [list, type(None)],
            'date_columns': [list, type(None)],
            'date_format': [str, type(None)],
            'category_columns': [list, type(None)]
        }

        error_message = '{} parameter should be of type {}; received {}.'

        for attribute, allowed_types in attribute_types.items():
            parameter = locals()[attribute]

            if any(isinstance(parameter, allowed_type) for allowed_type in allowed_types):
                continue
            raise TypeError(error_message.format(attribute, ' or '.join(allowed_types), parameter))

        return func(instance, name, type_, schema, monetary_columns, date_columns, date_format, category_columns)

    return table_validator
