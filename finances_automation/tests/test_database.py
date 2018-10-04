import os

import psycopg2

from finances_automation.database import Database


FINANCES_DATABASE = 'finances'
DATABASE_CLUSTER = os.path.join('..', '..', 'data', 'database_cluster')
USER = 'Marcus1'


def test_start():
    db = Database(FINANCES_DATABASE, DATABASE_CLUSTER, USER)
    db.create(overwrite=True)
    db.start()

    assert db.server_started

    db.stop()


def test_stop():
    db = Database(FINANCES_DATABASE, DATABASE_CLUSTER, USER)
    db.create(overwrite=True)
    db.start()
    db.stop()

    assert not db.server_started


def test_connect():
    db = Database(FINANCES_DATABASE, DATABASE_CLUSTER, USER)
    db.create(overwrite=True)
    db.start()

    assert isinstance(db.connection, psycopg2.extensions.connection)
    assert db.connection.closed == 0
    assert isinstance(db.cursor, psycopg2.extensions.cursor)
    assert not db.cursor.closed

    db.stop()


def test_disconnect():
    db = Database(FINANCES_DATABASE, DATABASE_CLUSTER, USER)
    db.create(overwrite=True)
    db.start()
    db.disconnect()

    assert db.connection.closed != 0
    assert db.cursor.closed

    db.stop()


def test_create():
    db = Database(FINANCES_DATABASE, DATABASE_CLUSTER, USER)
    db.create(overwrite=True)
    db.verify_existence()

    assert db.verified

    db.stop()
