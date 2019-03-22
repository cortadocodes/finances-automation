from finances_automation.validation.base import validate_variables


def database_validator(func):
    def database_validator(instance, host, name, cluster, user, password='', port=5432, log_location=None):
        """ Check if Database initialisation parameters are of correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'host': [str],
            'name': [str],
            'cluster': [str],
            'user': [str],
            'password': [str],
            'port': [int],
            'log_location': [str, type(None)]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, host, name, cluster, user, password, port, log_location)

    return database_validator
