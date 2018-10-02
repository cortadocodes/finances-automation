import psycopg2

from finances_automation.database import Database


def test_connect():
    db = Database('finances')
    db.connect()
    assert isinstance(db.connection, psycopg2.extensions.connection)
    assert db.connection.closed == 0
    assert isinstance(db.cursor, psycopg2.extensions.cursor)
    assert db.cursor.closed is False


def test_disconnect():
    db = Database('finances')
    db.connect()
    db.disconnect()
    assert db.connection.closed != 0
    assert db.cursor.closed is True
