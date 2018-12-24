""" Configuration constants for users of finances_automation; these determine how the database is set up,
which columns are relevant in statements, how dates are parsed, and which categories are applied to transactions.
"""
import os


PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
USER = 'Marcus1'

DB_NAME = 'finances'
DB_CLUSTER = os.path.join(PACKAGE_ROOT, 'data', 'database_cluster')

INCOME_CATEGORIES = [
    'job',
    'bursaries_and_scholarships',
    'transfers_in',
    'other_income',
]

EXPENSE_CATEGORIES = [
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
]

ADJUSTMENT_CATEGORIES = [
    'make_balance',
    'ignore'
]

CURRENT_TRANSACTIONS_TABLE = {
    'name': 'current_transactions',
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
    'monetary_columns': ['money_in', 'money_out', 'balance'],
    'date_columns': ['date'],
    'date_format': '%d/%m/%Y',
    'category_columns': ['category_code', 'category']
}

CREDIT_TRANSACTIONS_TABLE = {
    'name': 'credit_transactions',
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
    'monetary_columns': ['money_in', 'money_out', 'balance'],
    'date_columns': ['date'],
    'date_format': '%d/%m/%Y',
    'category_columns': ['category_code', 'category']
}

TOTALS_TABLE = {
    'name': 'totals',
    'schema': {
        'id': 'serial PRIMARY KEY',
        'start_date': 'DATE NOT NULL',
        'end_date': 'DATE NOT NULL',
        'analysis_date': 'DATE NOT NULL',
        **{
            category.lower().replace(' ', '_'): 'DECIMAL'
            for category in [*INCOME_CATEGORIES, *EXPENSE_CATEGORIES]
        }
    },
    'monetary_columns': [*INCOME_CATEGORIES, *EXPENSE_CATEGORIES],
    'date_columns': ['start_date', 'end_date', 'analysis_date'],
    'date_format': '%d/%m/%Y'
}

