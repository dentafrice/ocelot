from datetime import datetime, timedelta

from ocelot.lib import logging
from ocelot.services.constants.pipeline_schedule import PipelineScheduleTypes
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
        cls.update_last_run_at_for_pipeline(pipeline_id)
        cls.update_next_run_at_for_pipeline(pipeline_id)
        cls.unlock_schedule_for_pipeline(pipeline_id)

    @classmethod
    def update_last_run_at_for_pipeline(cls, pipeline_id):
        """Updates the last time a pipeline schedule was ran.

        :param str pipeline_id:
        """
        schedule = cls.fetch_schedule_for_pipeline(pipeline_id)
        schedule.last_run_at = datetime.utcnow()

        cls.write_pipeline_schedule(schedule)

    @classmethod
    def update_next_run_at_for_pipeline(cls, pipeline_id):
        """Updates the next_run_at time for a schedule.

        :param str pipeline_id:
        """
        schedule = cls.fetch_schedule_for_pipeline(pipeline_id)

        if schedule.type == PipelineScheduleTypes.cron:
            raise NotImplementedError
        elif schedule.type == PipelineScheduleTypes.interval:
            if not schedule.last_run_at:
                # schedule hasn't ran yet. let's set it to now.
                schedule.last_run_at = datetime.utcnow()

            schedule.next_run_at = (
                schedule.last_run_at + timedelta(
                    seconds=int(schedule.schedule),
                )
            )

        cls.write_pipeline_schedule(schedule)

    @classmethod
    def lock_schedule_for_pipeline(cls, pipeline_id):
        """Locks a schedule for a pipeline.

        :param str pipeline_id:
        """
        schedule = cls.fetch_schedule_for_pipeline(pipeline_id)
        schedule.locked = True

        cls.write_pipeline_schedule(schedule)

    @classmethod
    def unlock_schedule_for_pipeline(cls, pipeline_id):
        """Unlocks a schedule for a pipeline.

        :param str pipeline_id:
        """
        schedule = cls.fetch_schedule_for_pipeline(pipeline_id)
        schedule.locked = False

        cls.write_pipeline_schedule(schedule)

    @classmethod
    def write_pipeline_schedule(cls, pipeline_schedule_entity):
        """Writes a PipelineScheduleEntity to the database.

        :param PipelineScheduleEntity pipeline_schedule_entity:
        """
        cls._pre_write(pipeline_schedule_entity)
        cls._determine_changes(pipeline_schedule_entity)
        cls._write_entity(pipeline_schedule_entity)

    @classmethod
    def _pre_write(cls, entity):
        """Handles pre-write tasks like validation.

        :param PipelineScheduleEntity entity:
        """
        entity.validate()

    @classmethod
    def _write_entity(cls, entity):
        """Writes an entity to the repository.

        :param PipelineScheduleEntity entity:
        """
        PipelineScheduleRepository.write_record(
            PipelineScheduleMapper.to_record(entity),
        )

    @classmethod
    def _determine_changes(cls, new_entity):
        """Determine changes between the current entity and new entity.

        :param PipelineScheduleEntity new_entity:
        """
        current_entity = cls.fetch_schedule_for_pipeline(new_entity.pipeline_id)
        changes = {}

        for key, current_value in current_entity.items():
            new_value = new_entity.get(key)

            if new_value != current_value:
                changes[key] = (current_value, new_value)

        log.info('Updating pipeline: {} with changes {}'.format(
            new_entity.pipeline_id,
            changes,
        ))
