from finances_automation.entities.table import Table
from finances_automation.validation.base import validate_variables


def base_parser_validator(func):
    def base_parser_validator(instance, table, file):
        """ Check if BaseParser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'table': [Table],
            'file': [str]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, table, file)

    return base_parser_validator
