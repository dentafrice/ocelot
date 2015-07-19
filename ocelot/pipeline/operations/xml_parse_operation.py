import xml.etree.ElementTree as ET


class XMLParseOperation(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def write(self, data):
        """Accepteds and parses data from upstream.

        A string of XML will be parsed into an xml ElementTree and
        written to the output.

        :param data:
        """
        for item in data:
            self.output.write(
                [ET.fromstring(item)],
            )
