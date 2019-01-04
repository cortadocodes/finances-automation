from finances_automation import configuration as conf
from finances_automation.entities.database import Database
from finances_automation.entities.table import Table


class CreditTransactionsRepository:

    def __init__(self):
        """ Initialise a repository for the credit_transactions table.
        """
        self.db = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
        self.table = Table.get_table('credit_transactions')

    def insert(self, data):
        """ Insert data into the table.

        :param pandas.DataFrame data:
        """
        self.db.insert_into(
            table=self.table.name,
            columns=tuple(data.columns),
            values_group=data.itertuples(index=False)
        )
