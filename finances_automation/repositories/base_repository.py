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
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def load(self, start_date, end_date):
        self.table.data = self.db.select_from(self.table, columns=['*'], conditions=[
            ('{} >='.format(self.table.date_columns[0]), start_date),
            ('AND {} <='.format(self.table.date_columns[0]), end_date)
        ])

        self.table.data = pd.DataFrame(
            self.table.data, columns=self.table.schema.keys()
        )

        self.table.data = self.table.data.astype(
            dtype={column: float for column in self.table.monetary_columns}
        )

        self.table.data = self.table.data.astype({'category_code': float})

    def insert(self, data):
        """ Insert data into the table.

        :param pandas.DataFrame data:
        """
        self.db.insert_into(
            table=self.table.name,
            columns=tuple(data.columns),
            values_group=data.itertuples(index=False)
        )
