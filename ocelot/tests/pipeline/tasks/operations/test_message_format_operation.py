from ocelot.pipeline.tasks.operations import MessageFormatOperation
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'title': 't1', 'description': 'foobar'},
    {'title': 't2', 'description': 'foobar2'},
]


class TestMessageFormatOperation(TestCase):
    def test_process_formatted_message(self):
        """Test that process will process the formatted message to the output."""
        message = MessageFormatOperation(
            message='{{ data | map(attribute="title") | join(", ")}}',
        )

        self.assertEquals(
            message.process(FAKE_DICTS),
            't1, t2',
        )

    def test_process_single_dict(self):
        """Test that process works with a single dict instead of a list."""
        message = MessageFormatOperation(
            message='{{ data.title }}',
        )

        self.assertEquals(
            message.process(FAKE_DICTS[0]),
            't1',
        )
