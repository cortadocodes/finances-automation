from datetime import datetime
import pandas as pd

from finances_automation.entities.table import Table
from finances_automation.repositories import BaseRepository


class TestBaseRepository:

    table_config = {
        'name': 'test_table',
        'type_': 'test',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'date': 'DATE NOT NULL',
            'a': 'VARCHAR',
            'b': 'VARCHAR'
        }
    }

    table = Table(**table_config)

    example_data = pd.DataFrame(
        {
            'date': [
                datetime.date(date) for date in (datetime(2019, 1, 1), datetime(2019, 1, 2), datetime(2020, 1, 2))
            ],
            'a': ['1', '2', '3'],
            'b': ['4', '5', '6']
        }
    )

    def test_instantiation_and_connection(self):
        """ Ensure the repository can be instantiated and connected to the database.

        :return None:
        """
        BaseRepository(self.table)

    def test_create_table(self):
        """ Test that tables can be created.

        :raise AssertionError:
        :return None:
        """
        repository = BaseRepository(self.table)
        repository.create_table()
        assert repository.exists()

    def test_insert(self):
        """ Test insertion of data into a table.

        :raise AssertionError:
        :return None:
        """
        repository = BaseRepository(self.table)
        repository.create_table()

        repository.insert(self.example_data)

    def test_load(self):
        """ Ensure data can be loaded from a table.

        :raise AssertionError:
        :return None:
        """
        repository = BaseRepository(self.table)
        repository.create_table()

        repository.insert(self.example_data)
        repository.load('2019/1/1', '2020/1/2')

        assert all(self.table.data == self.example_data)
