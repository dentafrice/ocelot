from ocelot.lib.external.redis_lib import Redis
from ocelot.tests import TestCase


class TestRedisLib(TestCase):
    def test_get_returns_none_if_empty(self):
        """Test that no value is returned by get if it hasn't been saved."""
        self.assertIsNone(Redis.get('fake_key'))

    def test_set_saves_value(self):
        """Test that set saves the key with the value."""
        Redis.set('fake_key', 'fake_value')

        self.assertEquals(
            Redis.get('fake_key'),
            'fake_value',
        )
