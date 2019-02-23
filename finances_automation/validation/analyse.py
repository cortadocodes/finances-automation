from finances_automation.entities.table import Table
from finances_automation.validation.base import validate_variables


def analyser_validator(func):
    def analyser_validator(instance, analysis_type, tables_to_analyse, table_to_store, start_date, end_date):
        """ Check if Analyser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        allowed_parameter_types = {
            'analysis_type': [str],
            'table_to_analyse': [Table],
            'table_to_store': [Table, type(None)],
            'start_date': [str],
            'end_date': [str]
        }

        locals_ = locals()
        parameters = {parameter_name: locals_[parameter_name] for parameter_name in allowed_parameter_types}
        validate_variables(parameters, allowed_parameter_types)

        return func(instance, tables_to_analyse, table_to_store, analysis_type, start_date, end_date)

    return analyser_validator
