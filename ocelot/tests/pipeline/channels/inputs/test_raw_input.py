from ocelot.pipeline.channels.inputs import RawInput
from ocelot.tests import TestCase


class TestRawInput(TestCase):
    def test_data_saved(self):
        """Test that the passed in data is saved on the input."""
        input_channel = RawInput(
            data='fake_data',
        )

        self.assertEquals(
            input_channel.data,
            'fake_data',
        )

    def test_process_returns_data(self):
        """Test that the passed in data is returned when process is called."""
        input_channel = RawInput(
            data='fake_data',
        )

        self.assertEquals(
            input_channel.process('fake_input'),
            'fake_data',
        )
