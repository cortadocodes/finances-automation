import psycopg2


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

    def execute_statement(self, statement):
        if not isinstance(statement, str):
            raise TypeError('statement must be a string.')
        self.cursor.execute(statement)
        self.connection.commit()


FINANCES_DATABASE_NAME = 'finances'

create_transactions_table = """
    CREATE TABLE transactions (
         id serial PRIMARY KEY,
         date DATE NOT NULL,
         card VARCHAR,
         description VARCHAR,
         money_in DECIMAL,
         money_out DECIMAL,
         balance DECIMAL NOT NULL
    );
"""

database = Database(FINANCES_DATABASE_NAME)
database.connect()
database.execute_statement(create_transactions_table)
database.disconnect()
