from ocelot.pipeline.plumbing.fitting import Fitting


class Pipeline(object):
    def __init__(self, name):
        self.name = name

        self.fittings = []

    @property
    def input_fittings(self):
        """Returns list of input fittings that do not have sources.

        :returns list: input fittings.
        """
        return [
            fitting for fitting in self.fittings
            if fitting.is_input
        ]

    def add_task(self, task):
        """Adds a task to this pipeline via a Fitting.

        :param Task task:
        :returns Fitting: fitting for this task.
        """
        fitting = Fitting(
            task=task,
        )

        self.fittings.append(fitting)

        return fitting

    def run(self, data=None):
        """Passes the provided data to each of the input fittings. And starts the pipeline.

        :param data: data to pass.
        """
        for input_fitting in self.input_fittings:
            input_fitting.process(data)
