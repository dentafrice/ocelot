import uuid

from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.pipeline.plumbing.pipe import Pipe


class Fitting(object):
    def __init__(self, task, identifier=None):
        self.identifier = identifier or str(uuid.uuid4())
        self.task = task
        self.pipes = []

    @property
    def is_input(self):
        return self.task.is_input

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
        """Process data via the fitting's task and write it to the output pipes.

        :param data: data to process
        """
        response = self.task.process(data)

        try:
            for pipe in self.output_pipes:
                pipe.process(response)
        except StopProcessingException:
            pass
