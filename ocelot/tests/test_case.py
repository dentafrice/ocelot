import copy
import unittest

import charlatan
import mock
import fakeredis

from ocelot import config
from ocelot.services import datastores

database_engine = datastores.get_engine()
fixtures_manager = charlatan.FixturesManager(db_session=datastores.Session)


class TestCase(unittest.TestCase):
    """Default TestCase for Ocelot."""

    def __call__(self, *args, **kwargs):
        self._pre_test()

        with mock.patch.object(config, 'data', self._config_copy):
            unittest.TestCase.__call__(self, *args, **kwargs)

        self._post_test()

    def _pre_test(self):
        self._patch_redis()
        self._copy_config()

    def _post_test(self):
        pass

    def _copy_config(self):
        self._config_copy = copy.deepcopy(config.data)

    def _patch_redis(self):
        patcher = mock.patch(
            'ocelot.services.gateways.redis.RedisGateway.get_client',
            fakeredis.FakeStrictRedis
        )

        patcher.start()

        self.addCleanup(patcher.stop)
        self.addCleanup(self._clear_redis)

    def _clear_redis(self):
        fakeredis.FakeStrictRedis().flushall()

    def set_config(self, key, value):
        parts = key.split('.')
        config = self._config_copy

        for part in parts[:-1]:
            config.setdefault(part, {})
            config = config[part]

        config[parts[-1]] = value


class DatabaseTestCase(TestCase, charlatan.FixturesManagerMixin):
    fixtures_manager = fixtures_manager

    def _pre_test(self):
        self.init_fixtures()  # found in Charlatan
        self._setup_database()

        super(DatabaseTestCase, self)._pre_test()

    def _post_test(self):
        self._teardown_database()

        super(DatabaseTestCase, self)._post_test()

    def _setup_database(self):
        self.connection = database_engine.connect()

        datastores.initialize(engine=self.connection)
        datastores.create_tables(engine=self.connection)

        self.transaction = self.connection.begin()

    def _teardown_database(self):
        if hasattr(self, 'connection'):
            self.transaction.rollback()
            datastores.Session.remove()
            self.connection.close()
            del self.connection
