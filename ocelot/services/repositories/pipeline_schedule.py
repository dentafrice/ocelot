from datetime import datetime

from ocelot.services.datastores import NoResultFound, PipelineScheduleStore, Session
from ocelot.services.exceptions import ResourceNotFoundException


class PipelineScheduleRepository(object):
    @classmethod
    def fetch_schedule_for_pipeline(cls, pipeline_id):
        """Returns PipelineScheduleStore for a pipeline_id.

        :param str pipeline_id:
        :returns PipelineScheduleStore:
        """
        try:
            return (
                Session.query(PipelineScheduleStore)
                .filter(PipelineScheduleStore.pipeline_id == pipeline_id)
                .one()
            )
        except NoResultFound:
            raise ResourceNotFoundException

    @classmethod
    def fetch_schedules_to_run(cls):
        """Return a list of PipelineScheduleStores that need to run.

        :returns list: PipelineScheduleStore
        """
        return (
            Session.query(PipelineScheduleStore)
            .filter(PipelineScheduleStore.next_run_at <= datetime.utcnow())
            .filter(PipelineScheduleStore.locked == False)  # noqa
            .all()
        )

    @classmethod
    def write_record(cls, pipeline_record):
        """Writes a record to the database.

        :param PipelineScheduleStore pipeline_record:
        """
        Session.merge(pipeline_record)
        Session.commit()
