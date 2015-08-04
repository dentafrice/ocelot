from ocelot.pipeline.tasks.inputs.raw_input import RawInput
from ocelot.tests import TestCase


class TestRawInput(TestCase):
    def test_data_saved(self):
        """Test that the passed in data is saved on the input."""
        input_task = RawInput(
            data='fake_data',
        )

        self.assertEquals(
            input_task.data,
            'fake_data',
        )

    def test_process_returns_data(self):
        """Test that the passed in data is returned when process is called."""
        input_task = RawInput(
            data='fake_data',
        )

        self.assertEquals(
            input_task.process('fake_input'),
            'fake_data',
        )
