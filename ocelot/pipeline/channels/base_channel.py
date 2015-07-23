class BaseChannel(object):
    def __init__(self, id):
        self.id = id

    @property
    def is_input(self):
        return False

    @property
    def is_operation(self):
        return True

    @property
    def is_output(self):
        return False
