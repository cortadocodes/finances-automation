from finances_automation.database import Database
from finances_automation.scripts import configuration as conf


REQUIRE_OVERWRITE = False

CREATE_TABLE = (
    """
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
)


def initialise_database():
    """ Create and initialise a database with an empty table.
    """
    database = Database(conf.DB_NAME, conf.DB_CLUSTER, conf.USER)
    database.create(overwrite=REQUIRE_OVERWRITE)
    database.start()
    database.execute_statement(CREATE_TABLE)
    database.stop()


if __name__ == '__main__':
    initialise_database()
