from marrow.mailer import Mailer, Message

from ocelot import config


class SMTPGateway(object):
    @classmethod
    def send_email(cls, email_contents):
        """Sends an email via SMTP.

        :param dict email_contents:
            from_email
            to_email
            subject
            plain_message
            rich_message
        """
        mailer = Mailer({
            'manager.use': 'immediate',
            'transport.use': 'smtp',
            'transport.host': config.get('secrets.smtp.host'),
            'transport.port': config.get('secrets.smtp.port'),
            'transport.username': config.get('secrets.smtp.username'),
            'transport.password': config.get('secrets.smtp.password'),
            'transport.timeout': 10,
        })

        mailer.start()

        message = Message(
            author=email_contents['from_email'],
            to=email_contents['to_email'],
            subject=email_contents['subject'],
            plain=email_contents.get('plain_message') or '-- message not available --',
            rich=email_contents.get('rich_message'),
        )

        mailer.send(message)
        mailer.stop()
