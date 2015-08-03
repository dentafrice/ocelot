from sqlalchemy import Boolean, Column, DateTime, String

from ocelot.services.datastores import BaseStore, GUID


class PipelineScheduleStore(BaseStore):
    __tablename__ = 'pipeline_schedules'

    pipeline_id = Column(GUID, primary_key=True)

    schedule = Column(String)
    type = Column(String)

    next_run_at = Column(DateTime, index=True)
    last_run_at = Column(DateTime, index=True)

    locked = Column(Boolean, default=False, index=True)
