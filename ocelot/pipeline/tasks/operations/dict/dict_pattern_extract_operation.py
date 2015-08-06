import re

from ocelot.pipeline.exceptions import InvalidConfigurationException
from ocelot.pipeline.tasks.operations.dict.base_dict_operation import BaseDictOperation


class DictPatternExtractOperation(BaseDictOperation):
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
