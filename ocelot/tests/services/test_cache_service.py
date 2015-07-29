from freezegun import freeze_time

from ocelot.services.cache import CacheService
from ocelot.tests import TestCase


class TestCacheService(TestCase):
    def test_get_empty(self):
        """Test that None is returned if a key hasn't been saved."""
        self.assertIsNone(CacheService.fetch_value_for_key('fake_key'))

    def test_get_exists(self):
        """Test that the value is returned if a key has been saved."""
        CacheService.set_value_for_key('fake_key', 'fake_value')

        self.assertEquals(
            CacheService.fetch_value_for_key('fake_key'),
            'fake_value',
        )

    def test_ttl(self):
        """Test that a key can expire."""
        with freeze_time('2014-01-01T00:00:00'):
            CacheService.set_value_for_key('fake_key', 'fake_value', ttl=5)

            self.assertEquals(
                CacheService.fetch_value_for_key('fake_key'),
                'fake_value',
            )

        with freeze_time('2014-01-01T00:00:06'):
            self.assertIsNone(
                CacheService.fetch_value_for_key('fake_key'),
            )
