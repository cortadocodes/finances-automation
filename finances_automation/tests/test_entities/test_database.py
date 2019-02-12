import os
import shutil

import psycopg2
import pytest

from finances_automation.entities.database import Database


@pytest.mark.skip(reason='Slow to run.')
class TestDatabase:

    DATABASE_NAME = 'test_database'
    DATABASE_CLUSTER = os.path.join('..', '..', 'data', 'test_database_cluster')
    USER = 'Marcus1'

    def test_start(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.start()

        assert db.server_started

        db.stop()

    def test_stop(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.start()
        db.stop()

        assert not db.server_started

    def test_connect(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.start()

        assert isinstance(db.connection, psycopg2.extensions.connection)
        assert db.connection.closed == 0
        assert isinstance(db.cursor, psycopg2.extensions.cursor)
        assert not db.cursor.closed

        db.stop()

    def test_disconnect(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.start()
        db.disconnect()

        assert db.connection.closed != 0
        assert db.cursor.closed

        db.stop()

    def test_create(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.verify_existence()

        assert db.verified

        db.stop()
