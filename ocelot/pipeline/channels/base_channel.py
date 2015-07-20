class BaseChannel(object):
    @property
    def is_input(self):
        return False

    @property
    def is_operation(self):
        return True

    @property
    def is_output(self):
        return False
