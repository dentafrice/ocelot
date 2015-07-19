class BaseOperation(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def write(self, data):
        """Accepts and operates on data from upstream.

        :param data:
        """
        for item in data:
            self._process(item)

    def _process(self, data):
        """Process data in some way.

        :param data:
        """
        self._write(data)

    def _write(self, response):
        """Write response to output.

        :param response:
        """
        self.output.write([
            response
        ])
