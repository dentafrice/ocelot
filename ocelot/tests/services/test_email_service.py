import mock

from ocelot.services.email import EmailService, SMTPGateway
from ocelot.tests import TestCase


class TestEmailService(TestCase):
    @mock.patch.object(SMTPGateway, 'send_email')
    def test_send_email_calls_smtp_gateway(self, mock_send):
        """Test that the EmailService calls the SMTPGateway"""
        email_data = {
            'from_email': 'me@caleb.io',
            'to_email': 'me@caleb.io',
            'subject': 'sup',
            'plain_message': 'test',
        }

        EmailService.send_email(email_data)
        mock_send.assert_called_once_with(email_data)
