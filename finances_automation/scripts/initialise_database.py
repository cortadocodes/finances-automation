import os

from finances_automation.database import Database


PACKAGE_ROOT = os.path.abspath('..')
USER = 'Marcus1'

DB_NAME = 'finances'
DB_CLUSTER = os.path.join(PACKAGE_ROOT, '..', 'data', 'database_cluster')

TABLE_NAME = 'transactions'

OVERWRITE = True

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

CREATE_TRANSACTIONS_TABLE = (
    """
        CREATE TABLE {} (
             {} serial PRIMARY KEY,
             {} DATE NOT NULL,
             {} VARCHAR,
             {} VARCHAR,
             {} DECIMAL,
             {} DECIMAL,
             {} DECIMAL NOT NULL,
             {} INT,
             {} VARCHAR
        );
    """
    .format(DB_NAME, *TABLE_HEADERS)
)


def initialise_finances_database(db_name, db_cluster, user, table_creation_query):
    """ Create and initialise finances database with empty transactions table.
    """
    database = Database(db_name, db_cluster, user)
    database.create(overwrite=True)
    database.start()
    database.execute_statement(table_creation_query)
    database.stop()


if __name__ == '__main__':
    initialise_finances_database(DB_NAME, DB_CLUSTER, USER, CREATE_TRANSACTIONS_TABLE)
