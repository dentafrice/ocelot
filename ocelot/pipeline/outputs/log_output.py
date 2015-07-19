from ocelot.lib import logging

from ocelot.pipeline.outputs.base_output import BaseOutput


class LogOutput(BaseOutput):
    def __init__(self, log_name, *args, **kwargs):
        self._log_name = log_name

        super(LogOutput, self).__init__(*args, **kwargs)

    @property
    def log_name(self):
        """Returns the formatted log name.

        :returns str: log name
        """
        return 'ocelot.{}'.format(self._log_name)

    def _process(self, data):
        """Logs the data to a logger.

        :param data:
        """
        logging.getLogger(self.log_name).info(data)
