from __future__ import absolute_import

import logging
import logging.config

from ocelot import config

try:
    logging_config = config.get('logging').data
except AttributeError:
    logging_config = {}

logging.config.dictConfig(logging_config)


def getLogger(*args, **kwargs):
    """Returns a logger.

    This should be used so that we can ensure the logging configuration is setup.
    """
    return logging.getLogger(*args, **kwargs)
