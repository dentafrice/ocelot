from ocelot.pipeline.channels.operations import PluckOperation
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'foo': 'bar', 'bar': 'baz', 'title': 't1', 'description': 'd1'},
    {'foo': 'bar', 'bar': 'baz', 'title': 't2', 'description': 'd2'},
]


class TestPluckOperation(TestCase):
    def test_process_plucked_fields(self):
        """Test that process will process the plucked fields to the output."""
        pluck = PluckOperation(
            fields=['title', 'description'],
        )

        self.assertEquals(
            pluck.process(FAKE_DICTS),
            [
                {'title': 't1', 'description': 'd1'},
                {'title': 't2', 'description': 'd2'},
            ]
        )

    def test_process_single_dict(self):
        """Test that process works with a single dict instead of a list."""
        pluck = PluckOperation(
            fields=['title', 'description'],
        )

        self.assertEquals(
            pluck.process(FAKE_DICTS[0]),
            {'title': 't1', 'description': 'd1'},
        )
