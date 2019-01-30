from finances_automation.entities.table import Table


def base_parser_validator(func):
    def base_parser_validator(self, table, file):
        """ Check if BaseParser initialisation parameters are of the correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')
        if not isinstance(file, str):
            raise TypeError('file should be a string.')

        return func(self, table, file)

    return base_parser_validator
