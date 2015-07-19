import unittest

import mock
import fakeredis


class TestCase(unittest.TestCase):
    """Default TestCase for Ocelot."""

    def __call__(self, *args, **kwargs):
        self._patch_redis()

        unittest.TestCase.__call__(self, *args, **kwargs)

    def _patch_redis(self):
        patcher = mock.patch(
            'ocelot.lib.external.redis_lib.Redis.get_client',
            fakeredis.FakeStrictRedis
        )

        patcher.start()

        self.addCleanup(patcher.stop)
        self.addCleanup(self._clear_redis)

    def _clear_redis(self):
        fakeredis.FakeStrictRedis().flushall()
