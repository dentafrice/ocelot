import mock

from ocelot.lib.external.redis_lib import Redis
from ocelot.tests import TestCase


class TestRedisLib(TestCase):
    def setUp(self):
        self.fake_redis = mock.Mock()
        mock_get_client_patcher = mock.patch.object(
            Redis,
            'get_client',
            return_value=self.fake_redis,
        )

        self.mock_get_client = mock_get_client_patcher.start()

        self.addCleanup(mock_get_client_patcher.stop)

    def test_get_returns_value(self):
        """Test that a value is returned by get."""
        self.fake_redis.get.return_value = 'fake_value'

        self.assertEquals(
            Redis.get('fake_key'),
            'fake_value',
        )

        self.fake_redis.get.assert_called_once_with('fake_key')

    def test_set_saves_value(self):
        """Test that set saves the key with the value."""
        Redis.set('fake_key', 'fake_value')
        self.fake_redis.set.assert_called_once_with('fake_key', 'fake_value')
