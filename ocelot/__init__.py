from ocelot.lib import config_utils

BASE_CONFIG_FILENAME = '../config/base.yaml'


config = config_utils.Config(
    config_utils.load_config(
        config_utils.get_file_path(BASE_CONFIG_FILENAME, __file__),
    ),
)
