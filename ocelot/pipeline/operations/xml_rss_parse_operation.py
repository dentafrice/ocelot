class XMLRSSParseOperation(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def write(self, data):
        for item in data:
            return self.output.write([
                map(
                    self._convert_item_to_dict,
                    self._find_items(item),
                ),
            ])

    def _find_items(self, root_element):
        return root_element.findall('.//item')

    def _convert_item_to_dict(self, item):
        return {
            child.tag: child.text
            for child in item.getchildren()
        }
