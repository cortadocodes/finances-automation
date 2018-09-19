import psycopg2


FINANCES_DATABASE_NAME = 'finances'


def connect_to_database(dbname):
    connection = psycopg2.connect(dbname=dbname)
    cursor = connection.cursor()
    return connection, cursor


def create_transactions_table(connection, cursor):
    cursor.execute(
        """
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
    )
    connection.commit()


def disconnect_from_database(cursor, connection):
    cursor.close()
    connection.close()


connection, cursor = connect_to_database(FINANCES_DATABASE_NAME)
create_transactions_table(connection, cursor)
disconnect_from_database(cursor, connection)
