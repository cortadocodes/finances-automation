from finances_automation import configuration as conf
from finances_automation.entities.database import Database


class ParseRepository:

    def __init__(self):
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)

    def insert(self, data, table):
        """ Store the parsed transactions in a database table.

        :param pandas.DataFrame data:
        :param finances_automation.entities.Table table:
        """
        self.db.insert_into(
            table=table,
            columns=tuple(data.columns),
            values_group=data.itertuples(index=False)
        )
