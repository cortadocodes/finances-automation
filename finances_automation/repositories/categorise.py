import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class CategoriseRepository:

    def __init__(self):
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def update(self, table, data):
        self.db.start()

        for i in range(len(data)):
            id = int(data.iloc[i, 0])
            data = tuple([
                int(data.iloc[i][table.category_columns[0]]),
                data.iloc[i][table.category_columns[1]]]
            )

            operation = (
                """
                UPDATE {0}
                SET {1} = %s, {2} = %s
                WHERE {0}.id = {3}
                """
                    .format(
                    table.name,
                    table.category_columns[0],
                    table.category_columns[1],
                    id
                )
            )

            self.db.execute_statement(operation, data)

        self.db.stop()

    def load(self, table, start_date, end_date):
        data = self.db.select_from(table, columns=['*'], conditions=[
            ('{} >='.format(table.date_columns[0]), start_date),
            ('AND {} <='.format(table.date_columns[0]), end_date)
        ])

        data = pd.DataFrame(
            data, columns=table.schema.keys()
        )

        data = data.astype(
            dtype={column: float for column in table.monetary_columns}
        )

        data = data.astype({'category_code': float})

        return data
