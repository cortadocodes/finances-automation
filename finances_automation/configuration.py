""" Configuration constants for users of finances_automation; these determine how the database is set up,
which columns are relevant in statements, how dates are parsed, and which categories are applied to transactions.
"""
import os


package_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

db_config = {
    'host': 'localhost',
    'port': 5433,
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.environ['POSTGRES_PASSWORD']
}

categories = {
    'income': [
        'job',
        'bursaries_and_scholarships',
        'transfers_in',
        'other_income'
    ],

    'expense': [
        'rent',
        'utility_bills',
        'essentials',
        'health',
        'clothes',
        'subscriptions',
        'cash',
        'fun',
        'coffee',
        'holidays',
        'travel',
        'credit_card',
        'savings_and_investments',
        'loan_repayments',
        'charity',
        'other_expenses'
    ],

    'adjustment': [
        'make_balance',
        'ignore'
    ]
}

income_and_expense_categories = [*categories['income'], *categories['expense']]

table_configurations = {
    'current_transactions': {
        'name': 'current_transactions',
        'type_': 'transactions',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'date': 'DATE NOT NULL',
            'card': 'VARCHAR',
            'description': 'VARCHAR',
            'money_in': 'VARCHAR',
            'money_out': 'VARCHAR',
            'balance': 'DECIMAL',
            'category_code': 'DECIMAL',
            'category': 'VARCHAR'
        },
        'monetary_columns': {
            'money_in': 'money_in',
            'money_out': 'money_out',
            'balance': 'balance'
        },
        'date_columns': ['date'],
        'date_format': '%d/%m/%Y',
        'category_columns': ['category_code', 'category']
    },

    'credit_transactions': {
        'name': 'credit_transactions',
        'type_': 'transactions',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'date': 'DATE NOT NULL',
            'card': 'VARCHAR',
            'description': 'VARCHAR',
            'money_in': 'VARCHAR',
            'money_out': 'VARCHAR',
            'balance': 'DECIMAL',
            'category_code': 'DECIMAL',
            'category': 'VARCHAR'
        },
        'monetary_columns': {
            'money_in': 'money_in',
            'money_out': 'money_out',
            'balance': 'balance'
        },
        'date_columns': ['date'],
        'date_format': '%d/%m/%Y',
        'category_columns': ['category_code', 'category']
    },

    'totals': {
        'name': 'totals',
        'type_': 'analysis',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'tables_analysed': 'VARCHAR',
            'start_date': 'DATE NOT NULL',
            'end_date': 'DATE NOT NULL',
            'analysis_datetime': 'TIMESTAMPTZ NOT NULL',
            **{category: 'DECIMAL' for category in income_and_expense_categories}
        },
        'monetary_columns': {
            category: category for category in income_and_expense_categories
        },
        'date_columns': ['start_date', 'end_date', 'analysis_datetime'],
        'date_format': '%d/%m/%Y',
        'category_columns': None
    },

    'totals_across_all_accounts': {
        'name': 'totals_across_all_accounts',
        'type_': 'analysis',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'tables_analysed': 'VARCHAR',
            'start_date': 'DATE NOT NULL',
            'end_date': 'DATE NOT NULL',
            'analysis_datetime': 'TIMESTAMPTZ NOT NULL',
            **{category: 'DECIMAL' for category in income_and_expense_categories}
        },
        'monetary_columns': {
            category: category for category in income_and_expense_categories
        },
        'date_columns': ['start_date', 'end_date', 'analysis_datetime'],
        'date_format': '%d/%m/%Y',
        'category_columns': None
    },

    'monthly_averages': {
        'name': 'monthly_averages',
        'type_': 'analysis',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'tables_analysed': 'VARCHAR',
            'start_date': 'DATE NOT NULL',
            'end_date': 'DATE NOT NULL',
            'analysis_datetime': 'TIMESTAMPTZ NOT NULL',
            **{category: 'DECIMAL' for category in income_and_expense_categories}
        },
        'monetary_columns': {
            category: category for category in income_and_expense_categories
        },
        'date_columns': ['start_date', 'end_date', 'analysis_datetime'],
        'date_format': '%d/%m/%Y',
        'category_columns': None
    }
}


table_names = [table_name for table_name in table_configurations]

transaction_table_names = [
    table['name'] for table in list(table_configurations.values()) if table['type_'] == 'transactions'
]

analysis_table_names = [
    table['name'] for table in list(table_configurations.values()) if table['type_'] == 'analysis'
]

parser = {
    'delimiter': ',',
    'header': 3,
    'usecols': None,
    'dtype': None
}
