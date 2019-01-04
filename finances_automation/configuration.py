""" Configuration constants for users of finances_automation; these determine how the database is set up,
which columns are relevant in statements, how dates are parsed, and which categories are applied to transactions.
"""
import os

from finances_automation.repositories.credit_transactions import CreditTransactionsRepository
from finances_automation.repositories.current_transactions import CurrentTransactionsRepository
from finances_automation.repositories.monthly_averages import MonthlyAveragesRepository
from finances_automation.repositories.totals import TotalsRepository


PACKAGE_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DB_NAME = 'finances'
DB_CLUSTER = os.path.join(PACKAGE_ROOT, 'data', 'database_cluster')
USER = 'Marcus1'

CATEGORIES = {
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

TABLES = {
    'current_transactions': {
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
        'category_columns': ['category_code', 'category'],
        'repository': CurrentTransactionsRepository
    },

    'credit_transactions': {
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
        'category_columns': ['category_code', 'category'],
        'repository': CreditTransactionsRepository
    },

    'totals': {
        'name': 'totals',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'table_analysed': 'VARCHAR',
            'start_date': 'DATE NOT NULL',
            'end_date': 'DATE NOT NULL',
            'analysis_datetime': 'TIMESTAMPTZ NOT NULL',
            **{category: 'DECIMAL' for category in [*CATEGORIES['income'], *CATEGORIES['expense']]}
        },
        'monetary_columns': [*CATEGORIES['income'], *CATEGORIES['expense']],
        'date_columns': ['start_date', 'end_date', 'analysis_datetime'],
        'date_format': '%d/%m/%Y',
        'repository': TotalsRepository
    },

    'monthly_averages': {
        'name': 'monthly_averages',
        'schema': {
            'id': 'serial PRIMARY KEY',
            'table_analysed': 'VARCHAR',
            'start_date': 'DATE NOT NULL',
            'end_date': 'DATE NOT NULL',
            'analysis_datetime': 'TIMESTAMPTZ NOT NULL',
            **{category: 'DECIMAL' for category in [*CATEGORIES['income'], *CATEGORIES['expense']]}
        },
        'monetary_columns': [*CATEGORIES['income'], *CATEGORIES['expense']],
        'date_columns': ['start_date', 'end_date', 'analysis_datetime'],
        'date_format': '%d/%m/%Y',
        'repository': MonthlyAveragesRepository
    }
}

PARSER = {
    'delimiter': ',',
    'header': 3,
    'usecols': None,
    'dtype': None
}
