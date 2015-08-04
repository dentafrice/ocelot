from ocelot.pipeline.tasks.base_task import BaseTask


class BaseInput(BaseTask):
    def process(self, data):
        """Runs the input and returns the response data.

        :param object data:
        :returns object: response
        """
        raise NotImplementedError
