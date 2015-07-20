import uuid

from ocelot.pipeline.plumbing.pipe import Pipe


class Fitting(object):
    def __init__(self, channel, identifier=None):
        self.identifier = identifier or str(uuid.uuid4())
        self.channel = channel
        self.pipes = []

    @property
    def output_pipes(self):
        """Returns list of pipes that this fitting will write to.

        :returns list: output pipes
        """
        return [
            pipe for pipe in self.pipes
            if pipe.is_input(self)
        ]

    @property
    def source_pipes(self):
        """Returns list of pipes that this fitting will process data from.

        :returns list: source pipes
        """
        return [
            pipe for pipe in self.pipes
            if pipe.is_output(self)
        ]

    def add_pipe(self, pipe):
        """Adds a pipe to the internal collection.

        :param Pipe pipe:
        """
        self.pipes.append(pipe)

    def connect_fitting(self, fitting):
        """Connects a fitting to this fitting via a Pipe.

        :param Fitting fitting: fitting this pipe will write to.
        """
        pipe = Pipe(self, fitting)

        self.add_pipe(pipe)
        fitting.add_pipe(pipe)

    def process(self, data):
        """Process data via the fitting's channel and write it to the output pipes.

        :param data: data to process
        """
        response = self.channel.process(data)

        for pipe in self.output_pipes:
            pipe.process(response)
