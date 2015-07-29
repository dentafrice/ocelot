import copy
import unittest

import mock
import fakeredis

from ocelot import config


class TestCase(unittest.TestCase):
    """Default TestCase for Ocelot."""

    def __call__(self, *args, **kwargs):
        self._patch_redis()
        self._copy_config()

        with mock.patch.object(config, 'data', self._config_copy):
            unittest.TestCase.__call__(self, *args, **kwargs)

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
