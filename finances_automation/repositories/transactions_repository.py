from finances_automation.repositories.base_repository import BaseRepository


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
