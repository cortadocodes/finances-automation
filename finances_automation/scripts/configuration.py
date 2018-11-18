import os


PACKAGE_ROOT = os.path.abspath('..')
USER = 'Marcus1'

DB_NAME = 'finances'
DB_CLUSTER = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')

TABLE_NAME = 'transactions'

TABLE_HEADERS = [
    'id',
    'date',
    'card',
    'description',
    'money_in',
    'money_out',
    'balance',
    'category_code',
    'category'
]

MONETARY_COLUMNS = ['money_in', 'money_out', 'balance']
DATE_COLUMN = 'date'

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
