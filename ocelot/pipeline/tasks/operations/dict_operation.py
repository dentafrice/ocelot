import copy
import re

import jsonpath_rw

from ocelot.pipeline.tasks.operations.base_operation import BaseOperation
from ocelot.pipeline.exceptions import InvalidConfigurationException


class DictOperation(BaseOperation):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        super(DictOperation, self).__init__(*args, **kwargs)

    def process(self, data):
        """Perform operations on dictionaries.

        If `data` is a list:
            The operation will be applied to all elements in the list and a new list
            will be returned.

        Otherwise:
            The operation will be applied to `data`.

        :param data:
        :type data: list(dict) or dict
        :returns: processed data
        :rtype: list(dict) or dict
        """
        if isinstance(data, list):
            return map(self._process_item, data)
        else:
            return self._process_item(data)

    def _process_item(self, item):
        """Processes an individual dict by applying an operation to it.

        :param dict item:
        :returns dict: processed item
        """
        return self._perform_operation(
            copy.deepcopy(item),
        )

    def _perform_operation(self, item):
        """Stub method that performs the intended operation.

        :param dict item:
        :returns dict: processed item
        """
        raise NotImplementedError

    def _get_matches_for_paths(self, item, paths):
        """Returns list of matches for a list of paths.

        :param dict item:
        :param list paths:
        :returns list: JSONPath matches
        """
        matches = set()

        for path in paths:
            matches |= set(
                self._get_matches_for_path(item, path)
            )

        return list(matches)

    def _get_matches_for_path(self, item, path):
        """Returns list of matches for a path.

        :param dict item:
        :param str path: JSONPath path
        :returns list: JSONPath matches
        """
        return jsonpath_rw.parse(path).find(item)

    def _set_value_at_path(self, item, path, value):
        """Sets a value at a path in a dict.

        :param dict item:
        :param str path: JSONPath full path
            EX: foo.bar.baz or foo.[0].baz
        :param new_value: new value to set
        :type new_value: str or list or dict or None
        :returns dict: processed item
        """
        path = path.split('.')

        current_object = item

        for component in path[:-1]:
            if component.startswith('[') and component.endswith(']'):
                # current component is an array index
                index = int(component[1:-1])

                current_object = current_object[index]
            else:
                # current component is a sub key
                current_object = current_object[component]

        current_object[path[-1]] = value

        return item


class DictCreateOperation(DictOperation):
    def _perform_operation(self, item):
        """Creates and returns a new dict.

        The dict will contain one item with the key that
        is provided in the config, and the value passed to the operation.

        Example:
            ```
            operation = DictCreateOperation(
                config={
                    'key': 'fake-key',
                }
            )
            ```

            `operation.process('some-thing')` will return:
            ```
            {
                'fake-key': 'some-thing'
            }
            ```

        :param object item:
        :returns dict: constructed dict with key => item.
        """
        return {
            self.config['key']: item,
        }


class DictMapperOperation(DictOperation):
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


class DictPatternExtractOperation(DictOperation):
    def _perform_operation(self, item):
        """Runs a regex pattern on a value at a path to extract information.

        :param dict item:
        :returns dict: processed item
        """
        paths = self.config['paths']
        pattern = self.config['pattern']

        for match in self._get_matches_for_paths(item, paths):
            if not isinstance(match.value, basestring):
                raise InvalidConfigurationException(
                    'Match at `{}` is not a string'.format(
                        str(match.full_path),
                    )
                )

            matches = re.findall(pattern, match.value)
            new_value = matches[0] if matches else None

            item = self._set_value_at_path(item, str(match.full_path), new_value)

        return item
