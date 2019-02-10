def database_validator(func):
    def database_validator(self, name, data_location, user):
        """ Check if Database initialisation parameters are of correct type.

        :raise TypeError: if any of the parameters are of the wrong type
        """
        types = {
            'name': str,
            'data_location': str,
            'user':str
        }
        error_message = '{} parameter should be of type {}; received {}.'

        if not isinstance(name, types['name']):
            raise TypeError(error_message.format('name', types['name'], name))

        if not isinstance(data_location, types['data_location']):
            raise TypeError(error_message.format('data_location', types['data_location'], data_location))

        if not isinstance(user, types['user']):
            raise TypeError(error_message.format('user', types['user'], user))

        return func(self, name, data_location, user)

    return database_validator
