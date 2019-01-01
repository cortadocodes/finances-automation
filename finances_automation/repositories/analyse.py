import pandas as pd

from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class AnalyseRepository:

    def __init__(self):
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def load(self, table, start_date, end_date):
        data = self.db.select_from(table, columns=['*'], conditions=[
            ('{} >='.format(table.date_columns[0]), start_date),
            ('AND {} <='.format(table.date_columns[0]), end_date),
        ])

        data = pd.DataFrame(
            data, columns=table.schema.keys()
        ).astype(dtype={column: float for column in table.monetary_columns})

        return data

    def insert(self, table, analysis):
        self.db.insert_into(
            table,
            tuple(analysis.columns),
            analysis.itertuples(index=False)
        )
