class PluckOperation(object):
    def __init__(self, output, fields, *args, **kwargs):
        self.output = output
        self.fields = fields

    def write(self, data):
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
        return {
            field: value
            for field, value in item.items() if field in self.fields
        }
