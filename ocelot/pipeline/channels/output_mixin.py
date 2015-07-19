class OutputMixin(object):
    def __init__(self, output=None, *args, **kwargs):
        super(OutputMixin, self).__init__(*args, **kwargs)

        self._output = output

    @property
    def output(self):
        """Returns the output.

        :returns output:
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets output to be the new output.

        :param output:
        """
        self._output = output

    def _write(self, response):
        """Write response to output.

        :param response:
        """
        self._output.write([
            response,
        ])
