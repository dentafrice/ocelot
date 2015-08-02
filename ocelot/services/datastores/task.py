import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON

from ocelot.services.datastores import BaseStore, GUID


class TaskStore(BaseStore):
    __tablename__ = 'tasks'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    type = Column(String)
    config = Column(JSON)
