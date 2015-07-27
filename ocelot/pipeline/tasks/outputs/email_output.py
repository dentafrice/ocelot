from ocelot.pipeline.tasks.outputs.base_output import BaseOutput
from ocelot.services.email import EmailService


class EmailOutput(BaseOutput):
    def process(self, data):
        """Sends email via the EmailService.

        :param dict data:
            from_email
            to_email
            plain_message OR rich_message
        """
        EmailService.send_email({
            'from_email': data['from_email'],
            'to_email': data['to_email'],
            'subject': data['subject'],
            'plain_message': data.get('plain_message'),
            'rich_message': data.get('rich_message'),
        })
