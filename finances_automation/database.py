import psycopg2


class Database:
    """
    Create a PostgreSQL database wrapper object, allowing queries and commands to be passed in and data to be passed
    out.

    :param str name: pre-existing database name
    :param psycopg2.extensions.connection connection: connection to database
    :param psycopg2.extenstions.cursor cursor: cursor for executing SQL queries
    """
    def __init__(self, name):
        self.check_types(name)

        self.name = name
        self.connection = None
        self.cursor = None

    def check_types(self, name):
        """
        Check initialisation inputs are of correct type.

        :param any name: database name
        """
        if not isinstance(name, str):
            raise TypeError('name must be a string.')

    def connect(self):
        """
        Connect to the database.
        """
        self.connection = psycopg2.connect(dbname=self.name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """
        Disconnect from the database.
        """
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def execute_statement(self, statement, output_required=False):
        """
        Execute a SQL statement.

        :param str statement: valid SQL statement, command or query
        :param bool output_required: True if data is expected to be returned

        :return list: output from database due to statement
        """
        if not isinstance(statement, str):
            raise TypeError('statement must be a string.')

        self.cursor.execute(statement)

        if output_required:
            output = self.cursor.fetchall()
        else:
            output = None

        self.connection.commit()
        return output

    def describe(self):
        """
        Describe the database's structure (tables).

        :return list: table names and metadata
        """
        describe_statement = "SELECT * FROM information_schema.tables where table_schema = 'public'"
        tables = self.execute_statement(describe_statement, output_required=True)
        return tables
