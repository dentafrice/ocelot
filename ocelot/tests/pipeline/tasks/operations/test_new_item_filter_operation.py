from ocelot.pipeline.tasks.operations import NewItemFilterOperation
from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.tests import TestCase

FAKE_DATA = [
    'one',
    'two',
    'three',
]


class TestNewItemFilterOperation(TestCase):
    def test_process_allowed(self):
        """Test that when items haven't been
        seen before that they are returned."""
        new_item_filter = NewItemFilterOperation(
            identifier='fake_identifier',
        )

        self.assertEquals(
            new_item_filter.process(FAKE_DATA),
            FAKE_DATA,
        )

    def test_process_allowed_only_new(self):
        """Test that only new items that haven't been
        seen before are returned."""
        new_item_filter = NewItemFilterOperation(
            identifier='fake_identifier',
        )

        self.assertEquals(
            new_item_filter.process(FAKE_DATA[:2]),
            FAKE_DATA[:2],
        )

        self.assertEquals(
            new_item_filter.process(FAKE_DATA),
            [FAKE_DATA[-1]],
        )

    def test_no_new_raises_exception(self):
        """Test that StopProcessingException is raised if there are no new items."""
        new_item_filter = NewItemFilterOperation(
            identifier='fake_identifier',
        )

        new_item_filter.process(FAKE_DATA)

        with self.assertRaises(StopProcessingException):
            new_item_filter.process(FAKE_DATA)
