from ocelot.pipeline.tasks.base_task import BaseTask


class BaseInput(BaseTask):
    @property
    def is_input(self):
        return True

    def process(self, data):
        """Runs the input and writes the data to the output.

        :param data:
        :returns: response
        """
        raise NotImplementedError
