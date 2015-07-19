import mock

from ocelot.lib import cache
from ocelot.tests import TestCase


class TestCache(TestCase):
    @mock.patch('ocelot.lib.external.redis_lib.Redis.get')
    def test_get(self, mock_redis_get):
        """Test that Redis.get is called."""
        cache.get('fake_key')
        mock_redis_get.assert_called_once_with('fake_key')

    @mock.patch('ocelot.lib.external.redis_lib.Redis.set')
    def test_set(self, mock_redis_set):
        """Test that Redis.set is called."""
        cache.set('fake_key', 'fake_value')
        mock_redis_set.assert_called_once_with('fake_key', 'fake_value')
