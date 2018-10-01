import psycopg2


FINANCES_DATABASE_NAME = 'finances'


class Database:
    def __init__(self, name):
        self.check_types(name)

        self.name = name
        self.connection = None
        self.cursor = None

    def check_types(self, name):
        if not isinstance(name, str):
            raise TypeError('name must be a string.')

    def connect(self):
        self.connection = psycopg2.connect(dbname=self.name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def create_table(self, schema):
        if not isinstance(schema, str):
            raise TypeError('schema must be a string.')

        self.cursor.execute(schema)
        self.connection.commit()


database = Database(FINANCES_DATABASE_NAME)
database.connect()
database.disconnect()
