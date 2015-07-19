from ocelot.pipeline.channels.output_mixin import OutputMixin


class BaseInput(OutputMixin):
    def run(self):
        """Runs the input and writes the data to the output."""
        raise NotImplementedError
