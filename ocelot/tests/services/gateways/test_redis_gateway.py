from freezegun import freeze_time

from ocelot.services.gateways.redis import RedisGateway
from ocelot.tests import TestCase


class TestRedisGateway(TestCase):
    def test_get_returns_none_if_empty(self):
        """Test that no value is returned by get if it hasn't been saved."""
        self.assertIsNone(RedisGateway.fetch_value_for_key('fake_key'))

    def test_set_saves_value(self):
        """Test that set saves the key with the value."""
        RedisGateway.set_value_for_key('fake_key', 'fake_value')

        self.assertEquals(
            RedisGateway.fetch_value_for_key('fake_key'),
            'fake_value',
        )

    def test_set_expire(self):
        """Test that you can specify a TTL on a set and it will expire."""
        with freeze_time('2014-01-01T00:00:00'):
            RedisGateway.set_value_for_key('fake_key', 'fake_value', ttl=10)

            self.assertEquals(
                RedisGateway.fetch_value_for_key('fake_key'),
                'fake_value',
            )

        with freeze_time('2014-01-01T00:00:08'):
            self.assertEquals(
                RedisGateway.fetch_value_for_key('fake_key'),
                'fake_value',
            )

        with freeze_time('2014-01-01T00:00:11'):
            self.assertIsNone(
                RedisGateway.fetch_value_for_key('fake_key'),
            )
