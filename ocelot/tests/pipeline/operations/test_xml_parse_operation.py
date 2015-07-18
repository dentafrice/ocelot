from xml.etree.ElementTree import Element
import mock

from ocelot.pipeline.operations import XMLParseOperation
from ocelot.tests import TestCase

FAKE_XML = """
<root>
    <thing>heya</thing>
</root>
"""


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestXMLParseOperation(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_parsed_xml(self, mock_output_write):
        """Test that the output gets parsed XML written to it."""
        xml = XMLParseOperation(
            output=FakeOutput(),
        )

        xml.write([FAKE_XML])
        self.assertTrue(mock_output_write.called)

        parsed_element = mock_output_write.call_args[0][0][0]
        self.assertIsInstance(parsed_element, Element)
        self.assertEquals(parsed_element.tag, 'root')
