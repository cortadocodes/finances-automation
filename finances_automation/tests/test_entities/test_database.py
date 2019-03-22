import os
import shutil

import psycopg2
import pytest

from finances_automation.entities.database import Database


@pytest.mark.skip(reason='Slow to run.')
class TestDatabase:

    database_name = 'test_database'
    database_cluster = os.path.join('..', '..', 'data', 'test_database_cluster')
    database_user = 'Marcus1'

    db = Database(
        host='localhost',
        port=None,
        name=database_name,
        cluster=database_cluster,
        user=database_user,
        password=None
    )

    def teardown(self):
        if os.path.isdir(self.database_cluster):
            shutil.rmtree(self.database_cluster)

    def test_start(self):
        self.db.create()

        with self.db:
            assert self.db.is_started()

        self.teardown()

    def test_stop(self):
        self.db.create()
        self.db.start()
        self.db.stop()

        assert not self.db.is_started()

        self.teardown()

    def test_context_manager(self):
        self.db.create()

        with self.db:
            assert self.db.is_started()
        assert not self.db.is_started()

        self.teardown()

    def test_connect(self):
        self.db.create()

        with self.db:
            assert isinstance(self.db.connection, psycopg2.extensions.connection)
            assert self.db.connection.closed == 0
            assert isinstance(self.db.cursor, psycopg2.extensions.cursor)
            assert not self.db.cursor.closed

        self.teardown()

    def test_disconnect(self):
        self.db.create()

        with self.db:
            self.db.disconnect()
            assert self.db.connection.closed != 0
            assert self.db.cursor.closed

        self.teardown()

    def test_create(self):
        self.db.create()
        self.db.verify_existence()

        assert self.db.verified

        self.teardown()
