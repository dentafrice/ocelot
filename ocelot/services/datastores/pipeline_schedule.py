import uuid

from sqlalchemy import Boolean, Column, DateTime, String

from ocelot.services.datastores import BaseStore, GUID


class PipelineScheduleStore(BaseStore):
    __tablename__ = 'pipeline_schedules'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    pipeline_id = Column(GUID, index=True)

    schedule = Column(String)
    schedule_type = Column(String)

    next_run_at = Column(DateTime, index=True)
    last_run_at = Column(DateTime, index=True)

    locked = Column(Boolean, default=False, index=True)
