from ocelot.lib import logging
from ocelot.services.mappers.pipeline_schedule import PipelineScheduleMapper
from ocelot.services.repositories.pipeline_schedule import PipelineScheduleRepository

log = logging.getLogger('ocelot.pipeline_schedules')


class PipelineScheduleService(object):
    @classmethod
    def fetch_schedule_for_pipeline(cls, pipeline_id):
        """Returns a PipelineScheduleEntity for a pipeline_id.

        :param str pipeline_id:
        :returns PipelineScheduleEntity:
        :raises ResourceNotFoundException: if not found
        """
        return PipelineScheduleMapper.to_entity(
            PipelineScheduleRepository.fetch_schedule_for_pipeline(
                pipeline_id,
            ),
        )

    @classmethod
    def fetch_schedules_to_run(cls):
        """Return a list of PipelineScheduleEntities that need to run.

        :returns list: PipelineScheduleEntity
        """
        return map(
            PipelineScheduleMapper.to_entity,
            PipelineScheduleRepository.fetch_schedules_to_run(),
        )

    @classmethod
    def pre_run_schedule(cls, pipeline_id):
        """Set the schedule to running.

        Calling this will lock the schedule and prevent it from being
        picked up again by the scheduler.

        :param str pipeline_id:
        """
        cls.lock_schedule_for_pipeline(pipeline_id)

    @classmethod
    def post_run_schedule(cls, pipeline_id):
        """Set the schedule to not running.

        Calling this will unlock the schedule and allow it to be picked
        up again by the scheduler.

        It will update the next_run_at time according to the schedule.

        :param str pipeline_id:
        """
        # TODO: calculate next run time
        # TODO: set last_run_time = datetime.utcnow()
        cls.unlock_schedule_for_pipeline(pipeline_id)

    @classmethod
    def lock_schedule_for_pipeline(cls, pipeline_id):
        """Locks a schedule for a pipeline.

        :param str pipeline_id:
        """
        cls.update_schedule_for_pipeline(
            pipeline_id,
            {'locked': True},
        )

    @classmethod
    def unlock_schedule_for_pipeline(cls, pipeline_id):
        """Unlocks a schedule for a pipeline.

        :param str pipeline_id:
        """
        cls.update_schedule_for_pipeline(
            pipeline_id,
            {'locked': False},
        )

    @classmethod
    def update_schedule_for_pipeline(cls, pipeline_id, changes):
        """Updates a schedule for a pipeline.
        Schedule must already exist.

        :param str pipeline_id:
        :param dict changes:
        """
        log.info('Updating pipeline: {} with changes {}'.format(pipeline_id, changes))

        schedule = cls.fetch_schedule_for_pipeline(pipeline_id)

        for k, v in changes.items():
            setattr(schedule, k, v)

        cls.write_pipeline_schedule(schedule)

    @classmethod
    def write_pipeline_schedule(cls, pipeline_schedule_entity):
        """Writes a PipelineScheduleEntity to the database.

        :param PipelineScheduleEntity pipeline_schedule_entity:
        """
        pipeline_schedule_entity.validate()

        PipelineScheduleRepository.write_record(
            PipelineScheduleMapper.to_record(pipeline_schedule_entity),
        )
