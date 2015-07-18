import xml.etree.ElementTree as ET


class XMLParseOperation(object):
    def __init__(self, output, *args, **kwargs):
        self.output = output

    def write(self, data):
        for item in data:
            self.output.write(
                [ET.fromstring(item)],
            )
