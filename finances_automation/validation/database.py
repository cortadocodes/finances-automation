from finances_automation.validation.base import validate_variables


def database_validator(func):
    def database_validator(instance, host, port, name, cluster, user, password=None, log_location=None):
        """ Check if Database initialisation parameters are of correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'host': [str],
            'port': [str],
            'name': [str],
            'cluster': [str],
            'user': [str],
            'password': [str, type(None)],
            'log_location': [str, type(None)]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, host, port, name, cluster, user, password, log_location)

    return database_validator
