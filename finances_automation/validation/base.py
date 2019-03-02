def validate_variables(variables, allowed_variable_types):
    """ Validate that each variable in a dictionary is of the allowed types.

    :param dict(str, any) variables: variable name and variable
    :param dict(str, list(type)) allowed_variable_types: variable_name and list of allowed types
    :return None:
    """
    error_message = '{} parameter should be of type {}; received {}.'

    for variable_name, allowed_types in allowed_variable_types.items():
        variable = variables[variable_name]

        if any(isinstance(variable, allowed_type) for allowed_type in allowed_types):
            continue
        raise TypeError(error_message.format(variable_name, ' or '.join(allowed_types), variable))
