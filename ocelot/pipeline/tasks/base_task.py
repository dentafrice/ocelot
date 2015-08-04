import uuid


class BaseTask(object):
    def __init__(self, id=None):
        self.id = id or str(uuid.uuid4())
