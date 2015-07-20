from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseInput(BaseChannel):
    @property
    def is_input(self):
        return True

    def process(self, data):
        """Runs the input and writes the data to the output.

        :param data:
        :returns: response
        """
        raise NotImplementedError
