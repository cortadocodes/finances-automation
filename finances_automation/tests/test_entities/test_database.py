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

    def teardown(self):
        if os.path.isdir(self.DATABASE_CLUSTER):
            shutil.rmtree(self.DATABASE_CLUSTER)

    def test_start(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()

        with db:
            assert db.is_started()

        self.teardown()

    def test_stop(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.start()
        db.stop()

        assert not db.is_started()

        self.teardown()

    def test_context_manager(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()

        with db:
            assert db.is_started()
        assert not db.is_started()

        self.teardown()

    def test_connect(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()

        with db:
            assert isinstance(db.connection, psycopg2.extensions.connection)
            assert db.connection.closed == 0
            assert isinstance(db.cursor, psycopg2.extensions.cursor)
            assert not db.cursor.closed

        self.teardown()

    def test_disconnect(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()

        with db:
            db.disconnect()
            assert db.connection.closed != 0
            assert db.cursor.closed

        self.teardown()

    def test_create(self):
        db = Database(self.DATABASE_NAME, self.DATABASE_CLUSTER, self.USER)
        db.create()
        db.verify_existence()

        assert db.verified

        self.teardown()
