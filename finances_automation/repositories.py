import itertools

import pandas as pd
import psycopg2

from finances_automation import configuration as conf


class BaseRepository:
    """ A base repository that provides loading of data from a database table and insertion into it.
    """

    def __init__(self, table, db_config=None):
        """ Initialise a repository for the given table, connecting to the relevant database.

        :param finances_automation.entities.table.Table table:
        :param dict|None db_config:
        """
        self.table = table
        self.db_config = db_config or conf.db_config
        self.connection = psycopg2.connect(**self.db_config)

    def get_cursor(self):
        """ Get the database connection's cursor.

        :return psycopg2.extensions.cursor:
        """
        return self.connection.cursor()

    def commit(self):
        """ Commit any changes to the database.

        :return None:
        """
        self.connection.commit()

    def create_table(self):
        """ Create the table in the database.

        :return None:
        """
        if self.exists():
            return

        columns = self.table.schema.keys()
        column_schema_specifications = self.table.schema.values()
        schema_list = list(itertools.chain(*list(zip(columns, column_schema_specifications))))
        schema = ',\n'.join('{} {}' for _ in columns).format(*schema_list)

        query = 'CREATE TABLE {} ({});'.format(self.table.name, schema)

        with self.get_cursor() as cursor:
            cursor.execute(query)

    def exists(self):
        """ Does the table exist in the database?

        :return bool:
        """
        query = (
            """
            SELECT EXISTS
            (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = %s
            );
            """
        )

        with self.get_cursor() as cursor:
            cursor.execute(query, (self.table.name,))
            result = cursor.fetchone()

        return result[0] if result else False

    def load(self, start_date, end_date):
        """ Load data from the table between a start and end date (inclusive).

        :param str start_date:
        :param str end_date:
        :return None:
        """
        query = (
            """
            SELECT *
            FROM {}
            WHERE date >= %s
            AND date <= %s;
            """
            .format(self.table.name)
        )

        with self.get_cursor() as cursor:
            cursor.execute(
                query,
                (start_date, end_date)
            )

            data = cursor.fetchall()

        self.table.data = pd.DataFrame(data, columns=self.table.schema.keys())
        self.table.data.drop(['id'], axis=1, inplace=True)

        if self.table.monetary_columns:
            self.table.data = self.table.data.astype(
                dtype={column: float for column in self.table.monetary_columns.values()}
            )

        if self.table.category_columns:
            self.table.data = self.table.data.astype({'category_code': float})

    def insert(self, data, ignore_duplicates=True):
        """ Insert data into the table.

        :param pandas.DataFrame data:
        :param bool ignore_duplicates:
        :return None:
        """
        columns_placeholder = ', '.join(column for column in data.columns)
        values_placeholders = ', '.join(
            '(' + ', '.join('%s' for column in data.columns) + ')' for row in data.itertuples()
        )
        do_nothing_clause = 'ON CONFLICT DO NOTHING' if ignore_duplicates else ''

        query = 'INSERT INTO {} ({}) VALUES {} {};'.format(
            self.table.name,
            columns_placeholder,
            values_placeholders,
            do_nothing_clause
        )

        with self.get_cursor() as cursor:
            cursor.execute(query, tuple(itertools.chain(*data.itertuples(index=False))))


class TransactionsRepository(BaseRepository):
    """ A repository that provides updating of the category columns of a transactions database
    table, in addition to the methods of the base repository.
    """
    def get_latest_balance(self):

        query = (
            """
            SELECT balance FROM {}
            ORDER BY date DESC
            LIMIT 1
            """
            .format(self.table.name)
        )

        with self.get_cursor() as cursor:
            cursor.execute(query)
            latest_balance = cursor.fetchone()

        if latest_balance:
            return latest_balance[0]

    def get_latest_parsed_transaction_date(self):

        query = (
            """
            SELECT date FROM {}
            ORDER BY date DESC
            LIMIT 1
            """
            .format(self.table.name)
        )

        with self.get_cursor() as cursor:
            cursor.execute(query)
            latest_date = cursor.fetchone()

        if latest_date:
            return latest_date[0]

    def get_latest_categorised_transaction_date(self):

        query = (
            """
            SELECT date FROM {}
            WHERE {} is not NULL
            AND {} is not NULL
            ORDER BY date DESC
            LIMIT 1
            """
            .format(self.table.name, *self.table.category_columns)
        )

        with self.get_cursor() as cursor:
            cursor.execute(query)
            latest_date = cursor.fetchone()

            if latest_date:
                return latest_date[0]

    def update_categories(self):
        """ Update the table's category columns.
        """
        for i in range(len(self.table.data)):
            id_ = int(self.table.data.iloc[i, 0])
            row = self.table.data.iloc[i]

            values = tuple([
                int(row[self.table.category_columns[0]]),
                row[self.table.category_columns[1]]
            ])

            query = (
                """
                UPDATE {0}
                SET {1} = %s, {2} = %s
                WHERE {0}.id = {3}
                """
                .format(
                    self.table.name,
                    self.table.category_columns[0],
                    self.table.category_columns[1],
                    id_
                )
            )

            with self.get_cursor() as cursor:
                cursor.execute(query, values)
