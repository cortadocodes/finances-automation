from finances_automation.entities.table import Table


def database_validator(func):
    def database_validator(self, name, data_location, user):
        """ Check if Database initialisation parameters are of correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(name, str):
            raise TypeError('name must be a string.')
        if not isinstance(data_location, str):
            raise TypeError('data_location must be a string.')
        if not isinstance(user, str):
            raise TypeError('user must be a string.')

        return func(name, data_location, user)

    return database_validator


def table_validator(func):
    def table_validator(self, name, type, schema, monetary_columns, date_columns, date_format, category_columns):
        """ Check if Table initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(name, str):
            raise TypeError('name should be a string.')
        if not isinstance(type, str):
            raise TypeError('type should be a string')
        if not isinstance(schema, dict):
            raise TypeError('schema should be a dictionary.')
        if not isinstance(monetary_columns, list):
            raise TypeError('monetary_columns should be a list of strings.')
        if not isinstance(date_columns, list):
            raise TypeError('date_columns should be a list of strings.')
        if not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')
        if not isinstance(category_columns, list):
            raise TypeError('category_columns should be a list of strings.')

        return func(name, type, schema, monetary_columns, date_columns, date_format, category_columns)

    return table_validator


def base_parser_validator(func):
    def base_parser_validator(self, table, file):
        """ Check if BaseParser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(file, str):
            raise TypeError('file should be a string.')

        return func(table, file)

    return base_parser_validator


def categoriser_validator(func):
    def categoriser_validator(self, table, start_date, end_date, recategorise):
        """ Check if Categoriser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise TypeError('dates should be of type str.')
        if not isinstance(recategorise, bool):
            raise TypeError('recategorise should be boolean.')

        return func(table, start_date, end_date, recategorise)

    return categoriser_validator


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

        return func(tables_to_analyse, table_to_store, analysis_type, start_date, end_date)

    return analyser_validator
