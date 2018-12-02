class Table:

    def __init__(self, name, column_names, monetary_columns, date_column, date_format,
                  category_columns):

        self.name = name
        self.column_names = column_names
        self.monetary_columns = monetary_columns
        self.date_column = date_column
        self.date_format = date_format
        self.category_columns = category_columns

    @staticmethod
    def check_types(name, column_names, monetary_columns, date_column, date_format,
                    category_columns):

        if not isinstance(name, str):
            raise TypeError('name should be a string.')
        if not isinstance(column_names, list):
            raise TypeError('column_names should be a list of strings.')
        if not isinstance(monetary_columns, str):
            raise TypeError('monetary_columns should be a list of strings.')
        if not isinstance(date_column, str):
            raise TypeError('date_column should be a string.')
        if not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')
        if not isinstance(category_columns, str):
            raise TypeError('category_columns should be a list of strings.')
