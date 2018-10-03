import os
import subprocess

import psycopg2


class Database:
    """
    Create a PostgreSQL database wrapper object, allowing queries and commands to be passed in and data to be passed
    out.

    :param str name: pre-existing database name
    :param str data_location: path to database cluster
    :param psycopg2.extensions.connection connection: connection to database
    :param psycopg2.extenstions.cursor cursor: cursor for executing SQL queries
    """
    def __init__(self, name, data_location):
        self.check_types(name, data_location)

        self.name = name
        self.data_location = data_location
        self.server_started = False
        self.connection = None
        self.cursor = None

    def __repr__(self):
        repr = '{} database at {}: server_started = {}'.format(self.name, self.data_location, self.server_started)
        return repr

    def check_types(self, name, data_location):
        """
        Check initialisation inputs are of correct type.

        :param any name: database name
        :param any database_location: path to database cluster
        """
        if not isinstance(name, str):
            raise TypeError('name must be a string.')
        if not isinstance(data_location, str):
            raise TypeError('data_location must be a string.')

    def start(self):
        """
        Start PostgreSQL server.
        """
        subprocess.run(['pg_ctl', '-D', self.data_location, 'start'])
        server_status = subprocess.run(['pg_isready'], stdout=subprocess.PIPE).stdout
        if b'accepting connections' in server_status:
            self.server_started = True

    def stop(self):
        """
        Stop PostgreSQL server.
        """
        subprocess.run(['pg_ctl', '-D', self.data_location, 'stop'])
        server_status = subprocess.run(['pg_isready'], stdout=subprocess.PIPE).stdout
        if b'no response' in server_status:
            self.server_started = False

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
