from ocelot.lib import templating
from ocelot.pipeline.tasks.operations.base_operation import BaseOperation

FAKE_MESSAGE_NAME = 'fake_message_name'


class MessageFormatOperation(BaseOperation):
    def __init__(self, message, *args, **kwargs):
        self.message_value = message

        super(MessageFormatOperation, self).__init__(*args, **kwargs)

    def process(self, data):
        """Render message with provided data.

        :param data:
        :returns str message:
        """
        return templating.render_template(
            template_value=self.message_value,
            template_variables={
                'data': data,
            },
        )
