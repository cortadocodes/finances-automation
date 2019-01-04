import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


class CreditTransactionsRepository:

    def __init__(self):
        """ Initialise a repository for the credit_transactions table.
        """
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
        self.table = Table.get_table('credit_transactions')

    def load(self, start_date, end_date):
        self.data = self.db.select_from(self.table, columns=['*'], conditions=[
            ('{} >='.format(self.table.date_columns[0]), start_date),
            ('AND {} <='.format(self.table.date_columns[0]), end_date)
        ])

        self.data = pd.DataFrame(
            self.data, columns=self.table.schema.keys()
        )

        self.data = self.data.astype(
            dtype={column: float for column in self.table.monetary_columns}
        )

        self.data = self.data.astype({'category_code': float})

    def insert(self, data):
        """ Insert data into the table.

        :param pandas.DataFrame data:
        """
        self.db.insert_into(
            table=self.table.name,
            columns=tuple(data.columns),
            values_group=data.itertuples(index=False)
        )

    def update(self):
        self.db.start()

        for i in range(len(self.table.data)):
            id = int(self.table.data.iloc[i, 0])
            row = self.table.data.iloc[i]

            data = tuple([
                int(row[self.table.category_columns[0]]),
                row[self.table.category_columns[1]]]
            )

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
                    id
                )
            )

            self.db.execute_statement(operation, data)

        self.db.stop()
