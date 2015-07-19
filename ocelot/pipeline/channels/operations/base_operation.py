class BaseOperation(object):
    def process(self, data):
        """Accepts and operates on data from upstream.

        :param data:
        :returns: response
        """
        raise NotImplementedError
