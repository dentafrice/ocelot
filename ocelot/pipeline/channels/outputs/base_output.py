class BaseOutput(object):
    def process(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        raise NotImplementedError
