from ocelot.services.mappers.pipeline_schedule import PipelineScheduleMapper
from ocelot.services.repositories.pipeline_schedule import PipelineScheduleRepository


class PipelineScheduleService(object):
    @classmethod
    def fetch_schedules_for_pipeline(cls, pipeline_id):
        """Returns PipelineScheduleEntities for a pipeline_id.

        :param str pipeline_id:
        :returns list(PipelineScheduleEntity):
        """
        return map(
            PipelineScheduleMapper.to_entity,
            PipelineScheduleRepository.fetch_schedules_for_pipeline(pipeline_id),
        )
