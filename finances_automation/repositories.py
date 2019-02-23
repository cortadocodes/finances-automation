import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class BaseRepository:
    """ A base repository that provides loading of data from a database table and insertion into it.
    """

    def __init__(self, table):
        """ Initialise a repository for the given table.

        :param finances_automation.entities.table.Table table:
        """
        self.table = table
        self.db = Database(conf.db_name, conf.db_cluster, conf.user)

    def load(self, start_date, end_date):
        """ Load data from the table between a start and end date (inclusive).

        :param str start_date:
        :param str end_date:
        """
        self.table.data = self.db.select_from(self.table, columns=['*'], conditions=[
            ('{} >='.format(self.table.date_columns[0]), start_date),
            ('AND {} <='.format(self.table.date_columns[0]), end_date)
        ])

        self.table.data = pd.DataFrame(
            self.table.data, columns=self.table.schema.keys()
        )

        self.table.data = self.table.data.astype(
            dtype={column: float for column in self.table.monetary_columns.values()}
        )

        self.table.data = self.table.data.astype({'category_code': float})

    def insert(self, data):
        """ Insert data into the table.

        :param pandas.DataFrame data:
        """
        self.db.insert_into(
            table=self.table,
            columns=tuple(data.columns),
            values_group=data.itertuples(index=False)
        )


class TransactionsRepository(BaseRepository):
    """ A repository that provides updating of the category columns of a transactions database
    table, in addition to the methods of the base repository.
    """

    def update_categories(self):
        """ Update the table's category columns.
        """
        self.db.start()

        for i in range(len(self.table.data)):
            id_ = int(self.table.data.iloc[i, 0])
            row = self.table.data.iloc[i]

            data = tuple([
                int(row[self.table.category_columns[0]]),
                row[self.table.category_columns[1]]
            ])

            operation = (
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

            self.db.execute_statement(operation, data)

        self.db.stop()
