from ocelot.pipeline.channels.operations.base_operation import BaseOperation


class PluckOperation(BaseOperation):
    def __init__(self, fields, *args, **kwargs):
        self.fields = fields

        super(PluckOperation, self).__init__(*args, **kwargs)

    def process(self, data):
        """Pluck fields from a dict.

        :param dict data:
        :returns dict: response
        """
        if isinstance(data, list):
            return map(self._pluck, data)
        else:
            return self._pluck(data)

    def _pluck(self, item):
        """Plucks fields out of a dictionary.

        :param dict item:
        :returns dict: plucked dictionary
        """
        return {
            field: value
            for field, value in item.items() if field in self.fields
        }
