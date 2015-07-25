import xml.etree.ElementTree as ET

from ocelot.pipeline.tasks.operations import XMLRSSParseOperation
from ocelot.tests import TestCase

FAKE_RSS_XML = """
<rss>
    <task>
        <title>Fake thing</title>
        <item>
            <title>Fake Thing</title>
            <link>google.com</link>
        </item>

        <item>
            <title>Fake Thing 2</title>
            <link>google2.com</link>
        </item>
    </task>
</rss>
"""

FAKE_PARSED_XML = ET.fromstring(FAKE_RSS_XML)


class TestXMLRSSParseOperation(TestCase):
    def test_process_formatted_items(self):
        """Test that items are convert into dicts from the XML tree."""
        xml = XMLRSSParseOperation()

        self.assertEquals(
            xml.process(FAKE_PARSED_XML),
            [
                {'title': 'Fake Thing', 'link': 'google.com'},
                {'title': 'Fake Thing 2', 'link': 'google2.com'},
            ],
        )
