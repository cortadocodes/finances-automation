import os
import shutil

import psycopg2

from finances_automation.database import Database


DATABASE_NAME = 'test_database'
DATABASE_CLUSTER = os.path.join('..', '..', 'data', 'test_database_cluster')
USER = 'Marcus1'


def test_start():
    if os.path.isdir(DATABASE_CLUSTER):
        shutil.rmtree(DATABASE_CLUSTER)

    db = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    db.create()
    db.start()

    assert db.server_started

    db.stop()


def test_stop():
    if os.path.isdir(DATABASE_CLUSTER):
        shutil.rmtree(DATABASE_CLUSTER)

    db = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    db.create()
    db.start()
    db.stop()

    assert not db.server_started


def test_connect():
    if os.path.isdir(DATABASE_CLUSTER):
        shutil.rmtree(DATABASE_CLUSTER)

    db = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    db.create()
    db.start()

    assert isinstance(db.connection, psycopg2.extensions.connection)
    assert db.connection.closed == 0
    assert isinstance(db.cursor, psycopg2.extensions.cursor)
    assert not db.cursor.closed

    db.stop()


def test_disconnect():
    if os.path.isdir(DATABASE_CLUSTER):
        shutil.rmtree(DATABASE_CLUSTER)

    db = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    db.create()
    db.start()
    db.disconnect()

    assert db.connection.closed != 0
    assert db.cursor.closed

    db.stop()


def test_create():
    if os.path.isdir(DATABASE_CLUSTER):
        shutil.rmtree(DATABASE_CLUSTER)

    db = Database(DATABASE_NAME, DATABASE_CLUSTER, USER)
    db.create()
    db.verify_existence()

    assert db.verified

    db.stop()
