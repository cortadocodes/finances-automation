from finances_automation.entities.table import Table
from finances_automation.validation.base import validate_variables


def analyser_validator(func):
    def analyser_validator(instance, analysis_type, table_to_analyse, start_date, end_date, table_to_store=None):
        """ Check if Analyser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'analysis_type': [str],
            'table_to_analyse': [Table],
            'start_date': [str],
            'end_date': [str],
            'table_to_store': [Table, type(None)]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, analysis_type, table_to_analyse, start_date, end_date, table_to_store)

    return analyser_validator
