import xml.etree.ElementTree as ET

import mock

from ocelot.pipeline.operations import XMLRSSParseOperation
from ocelot.tests import TestCase

FAKE_RSS_XML = """
<rss>
    <channel>
        <title>Fake thing</title>
        <item>
            <title>Fake Thing</title>
            <link>google.com</link>
        </item>

        <item>
            <title>Fake Thing 2</title>
            <link>google2.com</link>
        </item>
    </channel>
</rss>
"""

FAKE_PARSED_XML = ET.fromstring(FAKE_RSS_XML)


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestXMLRSSParseOperation(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_formatted_items(self, mock_output_write):
        xml = XMLRSSParseOperation(
            output=FakeOutput(),
        )

        xml.write(FAKE_PARSED_XML)
        mock_output_write.assert_called_once_with([
            {'title': 'Fake Thing', 'link': 'google.com'},
            {'title': 'Fake Thing 2', 'link': 'google2.com'},
        ])
