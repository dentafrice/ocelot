from ocelot.pipeline.tasks.base_task import BaseTask


class BaseOutput(BaseTask):
    @property
    def is_output(self):
        return True

    def process(self, data):
        """Processes the data received from upstream.

        :param data:
        """
        raise NotImplementedError
