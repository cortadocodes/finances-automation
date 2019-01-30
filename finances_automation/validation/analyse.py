from finances_automation.entities.table import Table


def analyser_validator(func):
    def analyser_validator(self, tables_to_analyse, table_to_store, analysis_type, start_date, end_date):
        """ Check if Analyser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(tables_to_analyse, list):
            raise TypeError('table_to_analyse must be a list of Tables.')
        if not (isinstance(table_to_store, Table) or table_to_store is None):
            raise TypeError('table_to_store must be a Table or None.')
        if not isinstance(analysis_type, str):
            raise TypeError('analysis_type must be a string.')
        if not isinstance(start_date, str):
            raise TypeError('start_date must be a string.')
        if not isinstance(end_date, str):
            raise TypeError('end_date must be a string.')

        return func(self, tables_to_analyse, table_to_store, analysis_type, start_date, end_date)

    return analyser_validator
