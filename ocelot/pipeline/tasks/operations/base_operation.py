from ocelot.pipeline.tasks.base_task import BaseTask


class BaseOperation(BaseTask):
    def process(self, data):
        """Processes data in some way and returns the new data.

        :param object data:
        :returns object: response
        """
        raise NotImplementedError
