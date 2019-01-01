from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class ParseRepository:

    def __init__(self):
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def insert(self, table):
        """ Store the parsed transactions in a database table.
        """
        self.db.insert_into(
            table=table,
            columns=tuple(table.data.columns),
            values_group=table.data.itertuples(index=False)
        )
