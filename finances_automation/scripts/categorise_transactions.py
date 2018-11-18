import os
from finances_automation.categorise import Categoriser


PACKAGE_ROOT = os.path.abspath('..')
USER = 'Marcus1'

DB_NAME = 'finances'
DB_LOCATION = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')

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
c.load_from_database(TABLE_NAME, TABLE_HEADERS)
c.select_categories()

c.store_in_database(TABLE_NAME)

pass
