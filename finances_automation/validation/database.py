from finances_automation.validation.base import validate_variables


def database_validator(func):
    def database_validator(instance, name, data_location, user):
        """ Check if Database initialisation parameters are of correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'name': [str],
            'data_location': [str],
            'user': [str]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, name, data_location, user)

    return database_validator
