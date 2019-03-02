import itertools
import os
import re
import subprocess

import psycopg2

from finances_automation.entities.table import Table
from finances_automation.validation.database import database_validator


class Database:
    """ Create a PostgreSQL database wrapper object, allowing queries and commands to be passed in
    and data to be passed out.
    """

    # Location of bash script for creating psql database to connect to with Database object
    raw_repository_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).stdout
    repository_root = raw_repository_root.decode('ascii').strip()

    creation_script = os.path.join(repository_root, 'finances_automation', 'scripts', 'create_database.sh')

    @database_validator
    def __init__(self, name, data_location, user):
        """ Initialise a Database object for an existing or to-be-created PostgreSQL database.

        :param str name: database name
        :param str data_location: path to database cluster
        :param str user: name of database user

        :var bool server_started: indicates if psql server has been started
        :var bool verified: indicates that psql database does, in fact, exist
        :var bool connected: indicates Database object is connected to psql database
        :var bool cursor_connected: indicates cursor is connected to psql database
        :var psycopg2.extensions.connection connection: connection to database
        :var psycopg2.extensions.cursor cursor: cursor for executing SQL queries
        """

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

    def create_table(self, table):
        """ Create a database table from a Table object.

        :param finances_automation.entities.table.Table table: the table to create

        :raise TypeError: if the arguments are not of the correct type
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')

        columns = table.schema.keys()
        column_schema_specifications = table.schema.values()
        schema_list = list(itertools.chain(*list(zip(columns, column_schema_specifications))))

        schema = ',\n'.join(['{} {}' for _ in columns]).format(*schema_list)

        table_creation_statement = 'CREATE TABLE {} ({});'.format(table.name, schema)

        self.start()
        self.execute_statement(table_creation_statement)
        self.stop()

    def get_table_column_names(self, table):
        """ Get the column names of a table.

        :param Table table:

        :return list(str): column names
        """
        self.select_from(table, ['*'])
        return [description[0] for description in self.cursor.description]

    def select_from(self, table, columns, conditions=None):
        """ Select columns from a table according to conditions.

        :param Table table:
        :param list(str) columns:
        :param list(tuple) conditions:

        :return list(tuple): data from table
        """
        if not isinstance(table, Table):
            raise TypeError('table must be a Table.')

        if conditions:
            statement = 'SELECT {} FROM {} WHERE {};'.format(
                ','.join(columns),
                table.name,
                ' '.join(['{} %s'.format(condition[0]) for condition in conditions])
            )

            condition_values = tuple(condition[1] for condition in conditions)

        else:
            statement = 'SELECT {} FROM {};'.format(','.join(columns), table.name)
            condition_values = None

        self.start()
        data = self.execute_statement(statement, values=condition_values, output_required=True)
        self.stop()

        return data

    def insert_into(self, table, columns, values_group):
        """Insert values into columns of a table.

        :param Table table: database table to insert into
        :param tuple(str) columns: columns to insert into
        :param list(tuple) values_group: tuple of values for each row
        """
        self.start()

        for values in values_group:

            statement = (
                'INSERT INTO {} ({}) VALUES ({});'.format(
                    table.name,
                    ', '.join(['{}'] * len(columns)),
                    ', '.join(['%s'] * len(columns))
                )
                .format(*columns)
            )

            self.execute_statement(statement, values)

        self.stop()

    def execute_statement(self, statement, values=None, output_required=False):
        """
        Execute a SQL statement.

        :param str statement: valid SQL statement, command or query
        :param tuple values: values to pass to SQL statement or database
        :param bool output_required: True if data is expected to be returned

        :return list: output from database due to statement
        """
        if not isinstance(statement, str):
            raise TypeError('statement must be a string.')
        if not isinstance(output_required, bool):
            raise TypeError('output_required must be boolean.')

        self.cursor.execute(statement, values)

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

        # Find names of existing database (`psql -l`) and remove the headers (`-t`)
        raw_existing_dbs = subprocess.run(['psql', '-l', '-t'], stdout=subprocess.PIPE).stdout

        # Extract just the names into a list
        pattern = r'^\s+(\w+)\s+\|'
        existing_dbs = re.findall(pattern, raw_existing_dbs.decode('ascii'), flags=re.MULTILINE)

        if self.name in existing_dbs:
            self.verified = True
        else:
            self.verified = False

        if not initially_started:
            self.stop()
