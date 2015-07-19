class BaseOutput(object):
    def write(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        for item in data:
            self._process(item)

    def _process(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        raise NotImplementedError
