from ocelot.pipeline.channels.operations.base_operation import BaseOperation


class XMLRSSParseOperation(BaseOperation):
    def process(self, data):
        """Converts an Element into an array of dicts representing
        <item> elements.

        :param data:
        :returns list: list of dicts representing <item>s.
        """
        return map(
            self._convert_item_to_dict,
            self._find_items(data),
        )

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
