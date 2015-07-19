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
