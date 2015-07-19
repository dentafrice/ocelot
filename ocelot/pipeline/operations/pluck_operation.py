class PluckOperation(object):
    def __init__(self, output, fields, *args, **kwargs):
        self.output = output
        self.fields = fields

    def write(self, data):
        """Accepts and modifies data from upstream.

        Fields will be plucked out of a dictionary and a new dictionary
        will be written to the output.

        :param data:
        """
        for item in data:
            if isinstance(item, list):
                self.output.write([
                    map(self._pluck, item),
                ])

            else:
                self.output.write([
                    self._pluck(item),
                ])

    def _pluck(self, item):
        """Plucks fields out of a dictionary.

        :param dict item:
        :returns dict: plucked dictionary
        """
        return {
            field: value
            for field, value in item.items() if field in self.fields
        }
