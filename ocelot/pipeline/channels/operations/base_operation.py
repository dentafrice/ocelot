from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseOperation(BaseChannel):
    def process(self, data):
        """Accepts and operates on data from upstream.

        :param data:
        :returns: response
        """
        raise NotImplementedError
