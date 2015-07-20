from ocelot.pipeline.channels.base_channel import BaseChannel


class BaseOutput(BaseChannel):
    @property
    def is_output(self):
        return True

    def process(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        raise NotImplementedError
