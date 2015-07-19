import mock

from ocelot.pipeline.channels.inputs import URLInput
from ocelot.tests import TestCase


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestURLInput(TestCase):
    def test_output_stored(self):
        """Test that the provided output is stored on the URLInput."""
        fake_output = FakeOutput()
        url_input = URLInput(
            output=fake_output,
            url='fake_url',
        )

        self.assertEquals(url_input.output, fake_output)

    def test_url_stored(self):
        """Test that the provided url is stored on the URLInput."""
        fake_output = FakeOutput()
        url_input = URLInput(
            output=fake_output,
            url='fake_url',
        )

        self.assertEquals(url_input.url, 'fake_url')

    @mock.patch('requests.get')
    @mock.patch.object(FakeOutput, 'write')
    def test_run_writes_request_output(self, mock_write, mock_get):
        """Test that calling run writes the request content to the output."""
        fake_request = mock.MagicMock()
        type(fake_request).content = mock.PropertyMock(return_value='foobar')
        mock_get.return_value = fake_request

        fake_output = FakeOutput()
        url_input = URLInput(
            output=fake_output,
            url='fake_url',
        )

        url_input.run()
        mock_write.assert_called_once_with(['foobar'])

    @mock.patch('requests.get')
    def test_run_calls_provided_url(self, mock_get):
        """Test that calling run will make a request to the provided URL."""
        fake_output = FakeOutput()
        url_input = URLInput(
            output=fake_output,
            url='fake_url',
        )

        url_input.run()
        mock_get.assert_called_once_with('fake_url')
