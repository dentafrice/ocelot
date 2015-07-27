import mock

from ocelot.pipeline.tasks.outputs.email_output import EmailOutput, EmailService
from ocelot.tests import TestCase


class TestEmailOutput(TestCase):
    @mock.patch.object(EmailService, 'send_email')
    def test_send_email_calls_email_service(self, mock_send_email):
        """Test that send email calls the email service."""
        output = EmailOutput()

        output.process({
            'from_email': 'ocelot@caleb.io',
            'to_email': 'me@caleb.io',
            'subject': 'fake subject',
            'plain_message': 'plain message',
            'rich_message': 'rich message',
        })

        mock_send_email.assert_called_once_with({
            'from_email': 'ocelot@caleb.io',
            'to_email': 'me@caleb.io',
            'subject': 'fake subject',
            'plain_message': 'plain message',
            'rich_message': 'rich message',
        })
