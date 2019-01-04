from finances_automation.entities.table import Table
from finances_automation.repositories.base_repository import BaseRepository


class CurrentTransactionsRepository(BaseRepository):

    def __init__(self):
        """ Initialise a repository for the current_transactions table.
        """
        super().__init__()
        self.table = Table.get_table('totals')
