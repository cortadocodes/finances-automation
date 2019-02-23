from finances_automation.entities.table import Table
from finances_automation.validation.base import validate_variables


def categoriser_validator(func):
    def categoriser_validator(instance, table, start_date, end_date, recategorise=False):
        """ Check if Categoriser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'table': [Table],
            'start_date': [str],
            'end_date': [str],
            'recategorise': [bool]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, table, start_date, end_date, recategorise)

    return categoriser_validator
