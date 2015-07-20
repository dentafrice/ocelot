import uuid

from ocelot.pipeline.plumbing.pipe import Pipe


class Fitting(object):
    def __init__(self, channel, identifier=None):
        self.identifier = identifier or str(uuid.uuid4())
        self.channel = channel
        self.pipes = []

    @property
    def output_pipes(self):
        return [
            pipe for pipe in self.pipes
            if pipe.is_input(self)
        ]

    @property
    def source_pipes(self):
        return [
            pipe for pipe in self.pipes
            if pipe.is_output(self)
        ]

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def connect_fitting(self, fitting):
        pipe = Pipe(self, fitting)

        self.add_pipe(pipe)
        fitting.add_pipe(pipe)

    def process(self, data):
        response = self.channel.process(data)

        for pipe in self.output_pipes:
            pipe.process(response)
