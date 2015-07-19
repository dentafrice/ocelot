from ocelot.pipeline.channels.output_mixin import OutputMixin


class BaseInput(OutputMixin):
    def process(self, data):
        """Runs the input and writes the data to the output.

        :param data:
        :returns: response
        """
        raise NotImplementedError
