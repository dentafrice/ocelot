import mock

from ocelot.pipeline.channels.outputs import LogOutput
from ocelot.tests import TestCase

FAKE_DATA = [1, 2, 3]


class TestLogOutput(TestCase):
    def test_log_name(self):
        """Test that the provided log name is prefixed with ocelot."""
        log_output = LogOutput(
            log_name='foobar.baz',
        )

        self.assertEquals(log_output.log_name, 'ocelot.foobar.baz')

    @mock.patch('ocelot.lib.logging.getLogger')
    def test_write_sends_to_logger(self, mock_get_logger):
        """Test that calling write sends to the right logger."""
        fake_logger = mock.Mock()
        mock_get_logger.return_value = fake_logger

        log_output = LogOutput(
            log_name='foobar.baz',
        )

        log_output.write([FAKE_DATA])
        mock_get_logger.assert_called_once_with(log_output.log_name)
        fake_logger.info.assert_called_once_with(FAKE_DATA)
