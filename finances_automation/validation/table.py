from finances_automation.validation.base import validate_variables


def table_validator(func):
    def table_validator(instance, name, type_, schema, monetary_columns=None, date_columns=None, date_format=None,
                        category_columns=None):
        """ Check if Table initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'name': [str],
            'type_': [str],
            'schema': [dict],
            'monetary_columns': [list, type(None)],
            'date_columns': [list, type(None)],
            'date_format': [str, type(None)],
            'category_columns': [list, type(None)]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, name, type_, schema, monetary_columns, date_columns, date_format, category_columns)

    return table_validator
