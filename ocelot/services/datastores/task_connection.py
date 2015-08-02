import uuid

from sqlalchemy import Column

from ocelot.services.datastores import BaseStore, GUID


class TaskConnectionStore(BaseStore):
    __tablename__ = 'task_connections'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    from_task_id = Column(GUID, index=True)
    to_task_id = Column(GUID, index=True)
    pipeline_id = Column(GUID, index=True)
