from freezegun import freeze_time

from ocelot.lib import cache
from ocelot.tests import TestCase


class TestCache(TestCase):
    def test_get_empty(self):
        """Test that None is returned if a key hasn't been saved."""
        self.assertIsNone(cache.get('fake_key'))

    def test_get_exists(self):
        """Test that the value is returned if a key has been saved."""
        cache.set('fake_key', 'fake_value')

        self.assertEquals(
            cache.get('fake_key'),
            'fake_value',
        )

    def test_ttl(self):
        """Test that a key can expire."""
        with freeze_time('2014-01-01T00:00:00'):
            cache.set('fake_key', 'fake_value', ttl=5)

            self.assertEquals(
                cache.get('fake_key'),
                'fake_value',
            )

        with freeze_time('2014-01-01T00:00:06'):
            self.assertIsNone(
                cache.get('fake_key'),
            )
