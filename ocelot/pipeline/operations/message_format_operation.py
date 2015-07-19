from jinja2 import Environment, DictLoader

FAKE_MESSAGE_NAME = 'fake_message_name'


class MessageFormatOperation(object):
    def __init__(self, output, message, *args, **kwarsg):
        self.output = output
        self.message_value = message

    def write(self, data):
        """Accepts and formats data from upstream.

        Formatted message will be written to the output.

        :param data:
        """
        for item in data:
            message_environment = Environment(loader=DictLoader({
                FAKE_MESSAGE_NAME: self.message_value,
            }))

            message = message_environment.get_template(FAKE_MESSAGE_NAME)

            self.output.write([
                message.render({
                    'data': item,
                }),
            ])
