import os

from finances_automation.database import Database


DATABASE_NAME = 'finances'
DATABASE_CLUSTER = os.path.join('..', 'data', 'database_cluster')
USER = 'Marcus1'
OVERWRITE = True

CREATE_TRANSACTIONS_TABLE = """
    CREATE TABLE transactions (
         id serial PRIMARY KEY,
         date DATE NOT NULL,
         card VARCHAR,
         description VARCHAR,
         money_in DECIMAL,
         money_out DECIMAL,
         balance DECIMAL NOT NULL,
         category_code INT,
         category VARCHAR
    );
"""


def initialise_finances_database():
    """ Create and initialise finances database with empty transactions table.
    """
    database = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    database.create(overwrite=True)
    database.start()
    database.execute_statement(CREATE_TRANSACTIONS_TABLE)
    database.stop()


if __name__ == '__main__':
    initialise_finances_database()
