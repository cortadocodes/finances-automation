from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class ParseRepository:

    def __init__(self):
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def store(self, table, columns, values_group):
        """ Store the parsed transactions in a database table.
        """
        self.db.insert_into(
            table=table,
            columns=tuple(columns),
            values_group=values_group
        )
