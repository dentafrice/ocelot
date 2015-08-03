from ocelot.services.datastores import PipelineScheduleStore, Session


class PipelineScheduleRepository(object):
    @classmethod
    def fetch_schedules_for_pipeline(cls, pipeline_id):
        """Returns Pipeline schedules by pipeline_id.

        :param str pipeline_id:
        :returns list: PipelineScheduleStore
        """
        return (
            Session.query(PipelineScheduleStore)
            .filter(PipelineScheduleStore.pipeline_id == pipeline_id)
            .all()
        )

    @classmethod
    def write_record(cls, pipeline_record):
        """Writes a record to the database.

        :param PipelineScheduleStore pipeline_record:
        """
        Session.merge(pipeline_record)
        Session.commit()
