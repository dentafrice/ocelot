from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseInput(BaseChannel):
    def process(self, data):
        """Runs the input and writes the data to the output.

        :param data:
        :returns: response
        """
        raise NotImplementedError
