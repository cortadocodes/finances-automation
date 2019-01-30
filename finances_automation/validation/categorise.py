from finances_automation.entities.table import Table


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
