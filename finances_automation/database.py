import os
import re
import subprocess

import psycopg2


class Database:
    """
    Create a PostgreSQL database wrapper object, allowing queries and commands to be passed in and data to be passed
    out.

    :param str name: pre-existing database name
    :param str data_location: path to database cluster
    :param str user: name of database user
    :param bool server_started: indicates if psql server has been started
    :param bool verified: indicates that psql database does, in fact, exist
    :param bool connected: indicates Database object is connected to psql database
    :param bool cursor_connected: indicates cursor is connected to psql database
    :param psycopg2.extensions.connection connection: connection to database
    :param psycopg2.extensions.cursor cursor: cursor for executing SQL queries
    """

    # Location of bash script for creating psql database to connect to with Database object
    creation_script = os.path.join('..', 'scripts', 'create_database.sh')

    def __init__(self, name, data_location, user):
        self.check_types(name, data_location, user)

        # Database properties
        self.name = name
        self.data_location = data_location
        self.user = user

        # Database status indicators (relating to actual psql database and the connection to it)
        self.server_started = False
        self.verified = False
        self.connected = False
        self.cursor_connected = False

        # Python <-> psql connection objects
        self.connection = None
        self.cursor = None

    def __repr__(self):
        repr = '{} database at {}: server_started = {}'.format(self.name, self.data_location, self.server_started)
        return repr

    @staticmethod
    def check_types(name, data_location, user):
        """
        Check initialisation inputs are of correct type.

        :param any name: database name
        :param any data_location: path to database cluster
        :param any user: name of database user
        """
        if not isinstance(name, str):
            raise TypeError('name must be a string.')
        if not isinstance(data_location, str):
            raise TypeError('data_location must be a string.')
        if not isinstance(user, str):
            raise TypeError('user must be a string.')

    def create(self, overwrite=False):
        """
        Create a PostgreSQL database at self.data_location for self.user.

        :param bool overwrite: overwrite existing data in pre-existing data_location if True
        """
        if overwrite:
            overwrite = 'y'
        elif not overwrite:
            overwrite = 'n'
        else:
            raise TypeError("overwrite should be boolean")

        # Run database creation bash script
        subprocess.run(['bash', Database.creation_script, self.name, self.data_location, self.user, overwrite])

        self.verify_existence()
        if not self.verified:
            raise FileNotFoundError("Database creation not verified.")

    def start(self):
        """
        Start PostgreSQL server.
        """
        subprocess.run(['pg_ctl', '-D', self.data_location, 'start'])
        if not self.is_started():
            raise ConnectionError('Failed to start PostgreSQL server.')
        self.connect()

    def stop(self):
        """
        Stop PostgreSQL server.
        """
        self.disconnect()
        subprocess.run(['pg_ctl', '-D', self.data_location, 'stop'])
        if self.is_started():
            raise ConnectionError('Failed to stop PostgreSQL server.')

    def connect(self):
        """
        Connect to the database.
        """
        if not self.is_connected():
            self.connection = psycopg2.connect(dbname=self.name)
            if not self.is_connected():
                raise ConnectionError("Database connection unsuccessful.")

        if not self.is_cursor_connected():
            self.cursor = self.connection.cursor()
            if not self.is_cursor_connected():
                raise ConnectionError("Cursor connection unsuccessful.")

    def disconnect(self):
        """
        Disconnect from the database; if already disconnected, do nothing.
        """
        if self.is_cursor_connected():
            self.cursor.close()
            if self.is_cursor_connected():
                raise ConnectionError("Cursor disconnection unsuccessful.")

        if self.is_connected():
            self.connection.close()

            if self.is_connected():
                raise ConnectionError("Database disconnection unsuccessful.")

    def execute_statement(self, statement, output_required=False):
        """
        Execute a SQL statement.

        :param str statement: valid SQL statement, command or query
        :param bool output_required: True if data is expected to be returned

        :return list: output from database due to statement
        """
        if not isinstance(statement, str):
            raise TypeError('statement must be a string.')
        if not isinstance(output_required, bool):
            raise TypeError('output_required must be boolean.')

        self.cursor.execute(statement)

        if output_required:
            output = self.cursor.fetchall()
        else:
            output = None

        self.connection.commit()
        return output

    def is_started(self):
        """
        Check database has been started.

        :return bool: True if started
        """
        server_status = subprocess.run(['pg_isready'], stdout=subprocess.PIPE).stdout

        if b'accepting connections' in server_status:
            self.server_started = True
        elif b'no response' in server_status:
            self.server_started = False

        return self.server_started

    def is_connected(self):
        """
        Check database is connected to Database object.

        :return bool: True if connected
        """
        if hasattr(self.connection, 'closed'):
            if self.connection.closed == 0:
                self.connected = True
            else:
                self.connected = False
        else:
            self.connected = False

        return self.connected

    def is_cursor_connected(self):
        """
        Check cursor is connected to database.

        :return bool: True if connected.
        """
        if hasattr(self.cursor, 'closed'):
            if not self.cursor.closed:
                self.cursor_connected = True
            else:
                self.cursor_connected = False
        else:
            self.cursor_connected = False

        return self.cursor_connected

    def verify_existence(self):
        """
        Verify the database has actually been created.

        :return list: table names and metadata
        """
        initially_started = self.server_started
        if not initially_started:
            self.start()

        raw_existing_dbs = subprocess.run(['psql', '-l'], stdout=subprocess.PIPE).stdout

        pattern = r'^\s+(\w+)\s+\|'
        existing_dbs = re.findall(pattern, raw_existing_dbs.decode('ascii'), flags=re.MULTILINE)
        existing_dbs.remove('Name')

        if self.name in existing_dbs:
            self.verified = True
        else:
            self.verified = False

        if not initially_started:
            self.stop()
