from ocelot.pipeline.tasks.inputs.base_input import BaseInput


class RawInput(BaseInput):
    def __init__(self, data, *args, **kwargs):
        self.data = data

        super(RawInput, self).__init__(*args, **kwargs)

    def process(self, data):
        """Returns the provided data.

        :param data:
        :returns str: data
        """
        return self.data
