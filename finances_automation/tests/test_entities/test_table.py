import pytest

from finances_automation.entities.table import Table


class TestTable:
    def test_valid_table_instantiation(self):
        """ Test Table can be instantiated correctly without error.

        :raise AssertionError:
        :return None:
        """
        table = Table('a_table', 'a_type', {})
        assert not table.monetary_columns
        assert not table.date_columns
        assert not table.date_format
        assert not table.category_columns

    @pytest.mark.parametrize('name, type, schema, monetary_columns, date_columns, date_format, category_columns',[
        [None for _ in range(7)],
        [1, '', {}] + [None for _ in range(4)],
        ['', 1, {}] + [None for _ in range(4)],
        ['', '', set()] + [None for _ in range(4)],
        ['', '', {}, 1, [], '', []],
        ['', '', {}, [], 1, '', []],
        ['', '', {}, [], [], 1, []],
        ['', '', {}, [], [], '', 1],
    ])
    def test_invalid_table_instantiation(self, name, type, schema, monetary_columns, date_columns, date_format,
                                         category_columns):
        """ Test Table's validator raises the correct errors when instantiated with incorrect arguments.

        :raise AssertionError:
        :return:
        """
        with pytest.raises(TypeError):
            Table(name, type, schema, monetary_columns, date_columns, date_format, category_columns)
