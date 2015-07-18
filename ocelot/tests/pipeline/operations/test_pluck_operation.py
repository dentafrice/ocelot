import mock

from ocelot.pipeline.operations import PluckOperation
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'foo': 'bar', 'bar': 'baz', 'title': 't1', 'description': 'd1'},
    {'foo': 'bar', 'bar': 'baz', 'title': 't2', 'description': 'd2'},
]


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestPluckOperation(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_plucked_fields(self, mock_output_write):
        """Test that write will write the plucked fields to the output."""
        pluck = PluckOperation(
            output=FakeOutput(),
            fields=['title', 'description'],
        )

        pluck.write([FAKE_DICTS])

        mock_output_write.assert_called_once_with([[
            {'title': 't1', 'description': 'd1'},
            {'title': 't2', 'description': 'd2'},
        ]])

    @mock.patch.object(FakeOutput, 'write')
    def test_write_single_dict(self, mock_output_write):
        """Test that write works with a single dict instead of a list."""
        pluck = PluckOperation(
            output=FakeOutput(),
            fields=['title', 'description'],
        )

        pluck.write([FAKE_DICTS[0]])

        mock_output_write.assert_called_once_with([
            {'title': 't1', 'description': 'd1'},
        ])
