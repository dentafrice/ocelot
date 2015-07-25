from xml.etree.ElementTree import Element

from ocelot.pipeline.tasks.operations import XMLParseOperation
from ocelot.tests import TestCase

FAKE_XML = """
<root>
    <thing>heya</thing>
</root>
"""


class TestXMLParseOperation(TestCase):
    def test_process_parsed_xml(self):
        """Test that the output gets parsed XML written to it."""
        xml = XMLParseOperation()

        parsed_element = xml.process(FAKE_XML)
        self.assertIsInstance(parsed_element, Element)
        self.assertEquals(parsed_element.tag, 'root')
