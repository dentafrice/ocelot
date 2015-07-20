from ocelot.pipeline.plumbing.fitting import Fitting


class Pipeline(object):
    def __init__(self, name):
        self.name = name

        self.fittings = []

    @property
    def input_fittings(self):
        return [
            fitting for fitting in self.fittings
            if not len(fitting.source_pipes)
        ]

    def add_channel(self, channel):
        fitting = Fitting(
            channel=channel,
        )

        self.fittings.append(fitting)

        return fitting

    def run(self, data=None):
        for input_fitting in self.input_fittings:
            input_fitting.process(data)
