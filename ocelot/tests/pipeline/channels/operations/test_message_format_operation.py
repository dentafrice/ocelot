import mock

from ocelot.pipeline.channels.operations import MessageFormatOperation
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'title': 't1', 'description': 'foobar'},
    {'title': 't2', 'description': 'foobar2'},
]


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestMessageFormatOperation(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_formatted_message(self, mock_output_write):
        """Test that write will write the formatted message to the output."""
        message = MessageFormatOperation(
            output=FakeOutput(),
            message='{{ data | map(attribute="title") | join(", ")}}',
        )

        message.write([FAKE_DICTS])
        mock_output_write.assert_called_once_with(['t1, t2'])

    @mock.patch.object(FakeOutput, 'write')
    def test_write_single_dict(self, mock_output_write):
        """Test that write works with a single dict instead of a list."""
        message = MessageFormatOperation(
            output=FakeOutput(),
            message='{{ data.title }}',
        )

        message.write([FAKE_DICTS[0]])
        mock_output_write.assert_called_once_with(['t1'])
