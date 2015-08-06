from ocelot.pipeline.exceptions import InvalidConfigurationException
from ocelot.pipeline.tasks.operations.dict.base_dict_operation import BaseDictOperation


class DictMapperOperation(BaseDictOperation):
    def _perform_operation(self, item):
        """Creates a new dict based on the provided config.

        :param dict item:
        :returns dict: new constructed dict
        """
        new_dict = {}

        for key, field_config in self.config.items():
            op_type = field_config['type']

            if op_type == 'extract':
                new_dict[key] = self._extract(item, field_config['config'])
            elif op_type == 'insert':
                new_dict[key] = self._insert(item, field_config['config'])
            else:
                raise InvalidConfigurationException(
                    'Unknown operation type: `{}`'.format(
                        op_type,
                    )
                )

        return new_dict

    def _extract(self, item, field_config):
        """Extracts a value out of the item given a path.

        :param dict item:
        :param dict field_config:
        :returns object: value
        """
        matches = self._get_matches_for_path(
            item,
            field_config.get('path'),
        )

        return matches[0].value if matches else None

    def _insert(self, item, field_config):
        """Inserts a specified value at a key.

        :param dict item:
        :param dict field_config:
        :returns str: new value
        """
        return field_config.get('value')
