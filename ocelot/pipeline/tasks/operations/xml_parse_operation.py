import xml.etree.ElementTree as ET

from ocelot.pipeline.tasks.operations.base_operation import BaseOperation


class XMLParseOperation(BaseOperation):
    def process(self, data):
        """Parse a string of XML into an ElementTree Element.

        :param data:
        :returns Element:
        """
        return ET.fromstring(data)
