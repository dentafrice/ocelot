import json
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON

from ocelot.services.datastores import BaseStore, GUID


class TaskStore(BaseStore):
    __tablename__ = 'tasks'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    type = Column(String)
    _config = Column('config', JSON)

    @property
    def config(self):
        try:
            return json.loads(self._config)
        except TypeError:
            return {}

    @config.setter
    def config(self, value):
        self._config = value
