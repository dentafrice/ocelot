import os
import yaml


def get_file_path(filename, relative_file=None):
    """Returns an absolute file path given a filename and relative path.

    :param str filename:
    :param str relative_file:
    :returns str: file path
    """
    relative_file = relative_file or __file__

    return os.path.join(
        os.path.dirname(relative_file),
        filename,
    )


def load_config(file_path):
    """Loads and parses a YAML file at a path.

    Recursively loads extended (`extends`) files.

    :param str file_path:
    :returns dict:
    """
    with open(file_path, 'r') as f:
        config_data = yaml.safe_load(f) or {}

        if 'extends' in config_data:
            extends = config_data['extends']

            if not isinstance(extends, list):
                extends = [extends]

            for extend_filename in extends:
                extended_config_data = load_config(
                    get_file_path(
                        extend_filename,
                        relative_file=file_path,
                    ),
                )

                if extended_config_data:
                    extended_config_data.update(config_data)

                    config_data = extended_config_data

    return config_data


class Config():
    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        """Returns a value stored at a key.

        A key can have multiple components to reference nested objects.

        Example:

        {
            'foo': {
                'bar': {
                    'baz': 'hey',
                }
            }
        }

        config.get('foo.bar.baz') == 'hey'

        :param str key:
        :param default: (optional) default value if there is no value at key.
        :returns object: value stored at key
        """
        def _get(mapping, key_components):
            value = mapping

            for k in key_components:
                value = value[k]

            if isinstance(value, dict):
                return Config(value)

            return value

        key_components = key.split('.')

        try:
            return _get(self.data, key_components)
        except KeyError:
            return default
