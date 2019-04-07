import pandas as pd

from finances_automation.entities.table import Table
from finances_automation.repositories import BaseRepository


class TestBaseRepository:

    db_config = {
        'host': '0.0.0.0',
        'port': 63000,
        'dbname': 'postgres',
        'user': 'postgres',
    }

    table_config = {
        'name': 'test_table',
        'type_': 'test',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'a': 'VARCHAR',
            'b': 'VARCHAR'
        }
    }

    table = Table(**table_config)

    def test_instantiation_and_connection(self):
        """ Ensure the repository can be instantiated and connected to the database.

        :return None:
        """
        BaseRepository(self.table, self.db_config)

    def test_create_table(self):
        """ Test that tables can be created.

        :raise AssertionError:
        :return None:
        """
        repository = BaseRepository(self.table, self.db_config)
        repository.create_table()
        assert repository.exists()

    def test_insert(self):
        """ Test insertion of data into a table.

        :raise AssertionError:
        :return None:
        """
        repository = BaseRepository(self.table, self.db_config)
        repository.create_table()

        example_data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        repository.insert(example_data)
