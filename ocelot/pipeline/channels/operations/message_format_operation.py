from jinja2 import Environment, DictLoader

from ocelot.pipeline.channels.operations.base_operation import BaseOperation

FAKE_MESSAGE_NAME = 'fake_message_name'


class MessageFormatOperation(BaseOperation):
    def __init__(self, message, *args, **kwargs):
        self.message_value = message

        super(MessageFormatOperation, self).__init__(*args, **kwargs)

    def _process(self, data):
        """Render message with provided data.

        :param data:
        """
        message_environment = Environment(loader=DictLoader({
            FAKE_MESSAGE_NAME: self.message_value,
        }))

        message = message_environment.get_template(FAKE_MESSAGE_NAME)

        self._write(
            message.render({
                'data': data,
            }),
        )
