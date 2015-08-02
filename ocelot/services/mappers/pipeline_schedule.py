from ocelot.services.datastores import PipelineScheduleStore
from ocelot.services.entities.pipeline_schedule import PipelineScheduleEntity


class PipelineScheduleMapper(object):
    @staticmethod
    def to_entity(record):
        """Converts record into a PipelineScheduleEntity.

        :param PipelineScheduleStore record:
        :returns PipelineScheduleEntity:
        """
        return PipelineScheduleEntity({
            'id': record.id,
            'pipeline_id': record.pipeline_id,
            'schedule': record.schedule,
            'schedule_type': record.schedule_type,
            'next_run_at': record.next_run_at,
            'last_run_at': record.last_run_at,
            'locked': record.locked,
        })

    @staticmethod
    def to_record(entity):
        """Converts PipelineScheduleEntity into a record.

        :param PipelineScheduleEntity entity:
        :returns PipelineScheduleStore: record
        """
        return PipelineScheduleStore(**entity.to_native())
