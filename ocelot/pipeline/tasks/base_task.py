import uuid


class BaseTask(object):
    def __init__(self, id=None):
        self.id = id or str(uuid.uuid4())

    @property
    def is_input(self):
        return False

    @property
    def is_operation(self):
        return True

    @property
    def is_output(self):
        return False
