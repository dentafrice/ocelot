from ocelot.pipeline.channels.output_mixin import OutputMixin


class BaseOperation(OutputMixin):
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
