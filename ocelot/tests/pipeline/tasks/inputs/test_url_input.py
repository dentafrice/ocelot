import mock

from ocelot.pipeline.tasks.inputs import URLInput
from ocelot.tests import TestCase


class TestURLInput(TestCase):
    @mock.patch('requests.get')
    def test_run_processs_request_output(self, mock_get):
        """Test that calling run processs the request content to the output."""
        fake_request = mock.MagicMock()
        type(fake_request).content = mock.PropertyMock(return_value='foobar')
        mock_get.return_value = fake_request

        url_input = URLInput(
            url='fake_url',
        )

        self.assertEquals(
            url_input.process(None),
            'foobar',
        )

    @mock.patch('requests.get')
    def test_run_calls_provided_url(self, mock_get):
        """Test that calling run will make a request to the provided URL."""
        url_input = URLInput(
            url='fake_url',
        )

        url_input.process(None)
        mock_get.assert_called_once_with('fake_url')
