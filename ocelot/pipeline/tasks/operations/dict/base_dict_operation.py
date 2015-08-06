import copy
import jsonpath_rw

from ocelot.pipeline.tasks.operations.base_operation import BaseOperation


class BaseDictOperation(BaseOperation):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        super(BaseDictOperation, self).__init__(*args, **kwargs)

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
            return filter(
                self._allow_item,
                map(self._process_item, data),
            )
        else:
            processed_data = self._process_item(data)

            if self._allow_item:
                return processed_data

    def _allow_item(self, item):
        """Returns whether or not to allow an item to be returned from the operation.

        :param dict item:
        :returns boolean:
        """
        return True

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
