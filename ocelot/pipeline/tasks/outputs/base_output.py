from ocelot.pipeline.tasks.base_task import BaseTask


class BaseOutput(BaseTask):
    def process(self, data):
        """Takes the supplied data and outputs it somewhere.

        :param object data:
        """
        raise NotImplementedError
