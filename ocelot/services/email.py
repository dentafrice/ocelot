from ocelot.services.gateways.smtp import SMTPGateway


class EmailService(object):
    @classmethod
    def send_email(cls, email_contents):
        """Sends an email via the SMTPGateway.

        :param dict email_contents:
        """
        return SMTPGateway.send_email(email_contents)
