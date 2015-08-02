import os
import os.path

from ocelot.lib import config_utils

try:
    config_path = os.path.abspath(
        os.path.expandvars(
            os.environ['OCELOT_CONFIG'],
        )
    )
except KeyError:
    raise Exception('OCELOT_CONFIG is required')

config = config_utils.Config(
    config_utils.load_config(
        config_utils.get_file_path(config_path, __file__),
    ),
)
