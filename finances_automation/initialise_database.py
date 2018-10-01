from finances_automation.database import Database


FINANCES_DATABASE_NAME = 'finances'

create_transactions_table = """
    CREATE TABLE transactions (
         id serial PRIMARY KEY,
         date DATE NOT NULL,
         card VARCHAR,
         description VARCHAR,
         money_in DECIMAL,
         money_out DECIMAL,
         balance DECIMAL NOT NULL
    );
"""

database = Database(FINANCES_DATABASE_NAME)
database.connect()
database.execute_statement(create_transactions_table)
database.disconnect()
