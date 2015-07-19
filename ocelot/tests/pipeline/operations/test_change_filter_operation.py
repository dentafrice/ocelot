import mock

from ocelot.pipeline.operations import ChangeFilterOperation
from ocelot.tests import TestCase


FAKE_DATA = {'foo': 'bar', 'bar': 'baz'}


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestChangeFilterOperation(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_allowed(self, mock_output_write):
        """Test that when data has changed, it is written to the output."""
        change_filter = ChangeFilterOperation(
            output=FakeOutput(),
            identifier='fake_identifier',
        )

        change_filter.write([FAKE_DATA])
        mock_output_write.assert_called_once_with([FAKE_DATA])

    def test_write_not_allowed(self):
        """Test that when the data has not changed, it is written to the output."""
        change_filter = ChangeFilterOperation(
            output=FakeOutput(),
            identifier='fake_identifier',
        )

        with mock.patch.object(FakeOutput, 'write') as mock_write:
            change_filter.write([FAKE_DATA])
            mock_write.assert_called_once_with([FAKE_DATA])

        with mock.patch.object(FakeOutput, 'write') as mock_write:
            change_filter.write([FAKE_DATA])
            self.assertFalse(mock_write.called)
