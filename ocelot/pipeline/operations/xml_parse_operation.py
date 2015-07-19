import xml.etree.ElementTree as ET

from ocelot.pipeline.operations.base_operation import BaseOperation


class XMLParseOperation(BaseOperation):
    def _process(self, data):
        """Parse a string of XML into an ElementTree Element.

        :param data:
        """
        self._write(
            ET.fromstring(data),
        )
