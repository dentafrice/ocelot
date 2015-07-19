import copy
import re

from ocelot.pipeline.channels.operations.base_operation import BaseOperation


class DictPatternExtractor(BaseOperation):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        super(DictPatternExtractor, self).__init__(*args, **kwargs)

    def process(self, data):
        """Extract data by pattern from dict fields.

        :param dict data:
        :returns dict:
        """
        if isinstance(data, list):
            return map(self._extract, data)
        else:
            return self._extract(data)

    def _extract(self, item):
        """Extracts the data from the fields via the provided config.

        :param dict item:
        :returns dict: parsed item
        """
        item = copy.deepcopy(item)

        for field, pattern in self.config.items():
            matches = re.findall(pattern, item.get(field, ''))

            if matches:
                item[field] = matches[0]
            else:
                item[field] = ''

        return item
