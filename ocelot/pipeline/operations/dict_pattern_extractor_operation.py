import copy
import re


class DictPatternExtractor(object):
    def __init__(self, output, config, *args, **kwargs):
        self.output = output
        self.config = config

    def write(self, data):
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
        item = copy.deepcopy(item)

        for field, pattern in self.config.items():
            matches = re.findall(pattern, item.get(field, ''))

            if matches:
                item[field] = matches[0]
            else:
                item[field] = ''

        return item
