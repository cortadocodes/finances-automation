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
