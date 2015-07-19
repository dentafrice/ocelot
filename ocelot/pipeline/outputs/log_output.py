from ocelot.lib import logging


class LogOutput(object):
    def __init__(self, log_name, *args, **kwargs):
        self._log_name = log_name

    @property
    def log_name(self):
        """Returns the formatted log name.

        :returns str: log name
        """
        return 'ocelot.{}'.format(self._log_name)

    def write(self, data):
        """Accepts and logs data from upstream.

        :param data:
        """
        for item in data:
            logging.getLogger(self.log_name).info(item)
