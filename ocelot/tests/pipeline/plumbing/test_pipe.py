import mock

from ocelot.pipeline.plumbing.pipe import Pipe
from ocelot.tests import TestCase


class FakeFitting(object):
    def process(self, *args, **kwargs):
        pass


class TestPipe(TestCase):
    def setUp(self):
        self.fake_input = FakeFitting()
        self.fake_output = FakeFitting()
        self.pipe = Pipe(self.fake_input, self.fake_output)

    def test_input_fitting_saved(self):
        """Test that the input fitting is saved on the pipe."""
        self.assertEquals(
            self.pipe.input_fitting,
            self.fake_input,
        )

    def test_output_fitting_saved(self):
        """Test that the output fitting is saved on the pipe."""
        self.assertEquals(
            self.pipe.output_fitting,
            self.fake_output,
        )

    def test_is_input_true(self):
        """Test that is_input returns true when a fitting matches the input fitting."""
        self.assertTrue(
            self.pipe.is_input(self.fake_input)
        )

    def test_is_input_false(self):
        """Test that is_input returns false when a fitting does not matches the input fitting."""
        self.assertFalse(
            self.pipe.is_input(self.fake_output)
        )

    def test_is_output_true(self):
        """Test that is_output returns true when a fitting matches the output fitting."""
        self.assertTrue(
            self.pipe.is_output(self.fake_output)
        )

    def test_is_output_false(self):
        """Test that is_output returns false when a fitting does not matches the output fitting."""
        self.assertFalse(
            self.pipe.is_output(self.fake_input)
        )

    def test_process(self):
        """Test that process calls process on the output fitting with the data."""
        with mock.patch.object(self.fake_output, 'process') as mock_process:
            mock_process.return_value = 'fake_response'

            self.assertEquals(
                self.pipe.process('fake_data'),
                'fake_response',
            )

            mock_process.assert_called_once_with('fake_data')
