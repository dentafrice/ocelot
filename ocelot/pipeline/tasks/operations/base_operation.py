from ocelot.pipeline.tasks.base_task import BaseTask


class BaseOperation(BaseTask):
    @property
    def is_operation(self):
        return True

    def process(self, data):
        """Accepts and operates on data from upstream.

        :param data:
        :returns: response
        """
        raise NotImplementedError
