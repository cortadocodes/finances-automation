import os
from finances_automation.categorise import Categoriser


DB_NAME = 'finances'
PACKAGE_ROOT = os.path.abspath('..')
DB_LOCATION = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')
DB_TABLE = 'transactions'
USER = 'Marcus1'

DB_TABLE = 'transactions'
DB_TABLE_HEADERS = ['id', 'date', 'card', 'description', 'money_in', 'money_out', 'balance']

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


c = Categoriser(DB_NAME, DB_LOCATION, USER, INCOME_CATEGORIES, EXPENSE_CATEGORIES)
c.load_from_database(DB_TABLE, DB_TABLE_HEADERS)
c.select_categories()
c.store_in_database(DB_TABLE)

pass
