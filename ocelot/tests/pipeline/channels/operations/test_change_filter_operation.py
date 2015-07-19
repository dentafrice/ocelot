from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.pipeline.channels.operations import ChangeFilterOperation
from ocelot.tests import TestCase


FAKE_DATA = {'foo': 'bar', 'bar': 'baz'}


class TestChangeFilterOperation(TestCase):
    def test_process_allowed(self):
        """Test that when data has changed, it is written to the output."""
        change_filter = ChangeFilterOperation(
            identifier='fake_identifier',
        )

        self.assertEquals(
            change_filter.process(FAKE_DATA),
            FAKE_DATA,
        )

    def test_process_not_allowed(self):
        """Test that when the data has not changed, it is written to the output."""
        change_filter = ChangeFilterOperation(
            identifier='fake_identifier',
        )

        self.assertEquals(
            change_filter.process(FAKE_DATA),
            FAKE_DATA,
        )

        with self.assertRaises(StopProcessingException):
            change_filter.process(FAKE_DATA)
