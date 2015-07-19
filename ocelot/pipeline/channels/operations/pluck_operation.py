from ocelot.pipeline.channels.operations.base_operation import BaseOperation


class PluckOperation(BaseOperation):
    def __init__(self, fields, *args, **kwargs):
        self.fields = fields

        super(PluckOperation, self).__init__(*args, **kwargs)

    def _process(self, data):
        """Pluck fields from a dict.

        :param data:
        """
        if isinstance(data, list):
            self._write(
                map(self._pluck, data),
            )
        else:
            self._write(
                self._pluck(data),
            )

    def _pluck(self, item):
        """Plucks fields out of a dictionary.

        :param dict item:
        :returns dict: plucked dictionary
        """
        return {
            field: value
            for field, value in item.items() if field in self.fields
        }
