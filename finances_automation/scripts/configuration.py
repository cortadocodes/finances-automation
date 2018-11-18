import os


PACKAGE_ROOT = os.path.abspath('..')
USER = 'Marcus1'

DB_NAME = 'finances'
DB_CLUSTER = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')

TABLE_NAME = 'transactions'

TABLE_HEADERS = {
    'id': 'serial PRIMARY KEY',
    'date': 'DATE NOT NULL',
    'card': 'VARCHAR',
    'description': 'VARCHAR',
    'money_in': 'VARCHAR',
    'money_out': 'VARCHAR',
    'balance': 'DECIMAL NOT NULL',
    'category_code': 'INT',
    'category': 'VARCHAR'
}

MONETARY_COLUMNS = ['money_in', 'money_out', 'balance']

DATE_COLUMN = 'date'
DATE_FORMAT = '%d/%m/%Y'

CATEGORY_COLUMNS = ['category_code', 'category']

INCOME_CATEGORIES = [
    'Job',
    'Bursaries/scholarships',
    'Transfers in',
    'Other income',
]

EXPENSE_CATEGORIES = [
    'Rent',
    'Utility bills',
    'Essentials',
    'Health',
    'Clothes',
    'Subscriptions',
    'Cash',
    'Fun',
    'Coffee',
    'Holidays',
    'Travel',
    'Credit card',
    'Savings/investments',
    'Loan repayments',
    'Charity',
    'Other expenses'
]
