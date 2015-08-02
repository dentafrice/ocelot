import uuid

from sqlalchemy import Column, String

from ocelot.services.datastores import BaseStore, GUID


class PipelineStore(BaseStore):
    __tablename__ = 'pipelines'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
