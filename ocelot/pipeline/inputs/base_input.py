class BaseInput(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def run(self):
        """Runs the input and writes the data to the output."""
        raise NotImplementedError

    def _write(self, response):
        self.output.write([
            response,
        ])
