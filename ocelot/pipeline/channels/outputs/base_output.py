from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseOutput(BaseChannel):
    def process(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        raise NotImplementedError
