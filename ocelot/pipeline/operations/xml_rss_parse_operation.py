class XMLRSSParseOperation(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def write(self, data):
        """Accepts and parses data from upstream.

        Data will be converted from an ElementTree into
        an array of dictionaries representing item elements.

        :param data:
        """
        for item in data:
            return self.output.write([
                map(
                    self._convert_item_to_dict,
                    self._find_items(item),
                ),
            ])

    def _find_items(self, root_element):
        """Find all <item> elements in this ElementTree.

        :param Element root_element:
        :returns list: list of <item> Elements
        """
        return root_element.findall('.//item')

    def _convert_item_to_dict(self, item):
        """Converts an Element to a dict.

        :param Element item:
        :returns dict: parsed Element
        """
        return {
            child.tag: child.text
            for child in item.getchildren()
        }
