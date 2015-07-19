import copy
import re


class DictPatternExtractor(object):
    def __init__(self, output, config, *args, **kwargs):
        self.output = output
        self.config = config

    def write(self, data):
        """Accepts and extracts data from upstream.
        Data can be pulled out of dict fields and parsed via regex.

        Parsed data will be written to the provided output.

        :param data:
        """
        for item in data:
            if isinstance(item, list):
                self.output.write([
                    map(self._extract, item),
                ])
            else:
                self.output.write([
                    self._extract(item)
                ])

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
