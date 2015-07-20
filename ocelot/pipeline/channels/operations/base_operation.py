from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseOperation(BaseChannel):
    @property
    def is_operation(self):
        return True

    def process(self, data):
        """Accepts and operates on data from upstream.

        :param data:
        :returns: response
        """
        raise NotImplementedError
