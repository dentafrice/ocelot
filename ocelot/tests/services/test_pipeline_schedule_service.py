from datetime import datetime, timedelta
import mock

from freezegun import freeze_time

from ocelot.services.pipeline_schedule import (
    PipelineScheduleMapper,
    PipelineScheduleService,
)
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleService(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')
        self.install_fixture('pipeline_schedule_interval')

    def test_fetch_schedule_for_pipeline(self):
        """Test that you can fetch schedules for a pipeline."""
        self.assertEqual(
            PipelineScheduleService.fetch_schedule_for_pipeline(
                self.pipeline.id,
            ),

            PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval),
        )

    def test_fetch_schedules_to_run(self):
        """Test that schedules that need to run are returned."""
        self.assertEqual(
            PipelineScheduleService.fetch_schedules_to_run(),
            [
                PipelineScheduleMapper.to_entity(
                    self.pipeline_schedule_interval,
                ),
            ],
        )

    @mock.patch.object(PipelineScheduleService, 'lock_schedule_for_pipeline')
    def test_pre_run_schedule_locks(self, mock_lock):
        """Test that the schedule is locked."""
        PipelineScheduleService.pre_run_schedule(self.pipeline.id)
        mock_lock.assert_called_once_with(self.pipeline.id)

    @mock.patch.object(PipelineScheduleService, 'unlock_schedule_for_pipeline')
    def test_post_run_schedule_unlocks(self, mock_unlock):
        """Test that the schedule is locked."""
        PipelineScheduleService.post_run_schedule(self.pipeline.id)
        mock_unlock.assert_called_once_with(self.pipeline.id)

    @mock.patch.object(PipelineScheduleService, 'update_last_run_at_for_pipeline')
    def test_post_run_updates_last_run_at(self, mock_update):
        """Test that last_run_at is updated."""
        PipelineScheduleService.post_run_schedule(self.pipeline.id)
        mock_update.assert_called_once_with(self.pipeline.id)

    @mock.patch.object(PipelineScheduleService, 'update_next_run_at_for_pipeline')
    def test_post_run_updates_next_run_at(self, mock_update):
        """Test that next_run_at is updated."""
        PipelineScheduleService.post_run_schedule(self.pipeline.id)
        mock_update.assert_called_once_with(self.pipeline.id)

    @freeze_time('2014-02-01')
    def test_update_last_run_at(self):
        """Test that last_run_at is updated to the latest date."""
        # Assert that last_run_at is empty
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'last_run_at',
            None,
        )

        # Set last_run_at to expected
        PipelineScheduleService.update_last_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Assert that last_run_at is expected
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'last_run_at',
            datetime(2014, 02, 01),
        )

    @freeze_time('2014-02-01')
    def test_update_next_run_at_cron(self):
        """Test that next_run_at = croniter parse."""
        self.uninstall_fixture('pipeline_schedule_interval')
        self.install_fixture('pipeline_schedule_cron')

        # Set last_run_at to expected
        PipelineScheduleService.update_last_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Update next_run_at
        PipelineScheduleService.update_next_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Assert that next_run_at is expected
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'next_run_at',
            datetime(2014, 2, 1, 0, 5),
        )

    @freeze_time('2014-02-01')
    def test_update_next_run_at_interval(self):
        """Test that next_run_at = last_run_at + interval."""
        # Update last_run_at
        PipelineScheduleService.update_last_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Update next_run_at
        PipelineScheduleService.update_next_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Assert next_run_at is updated to last_run_at + interval
        schedule = PipelineScheduleService.fetch_schedule_for_pipeline(
            self.pipeline.id,
        )

        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'next_run_at',
            schedule.last_run_at + timedelta(seconds=int(schedule.schedule)),
        )

    @freeze_time('2014-03-01')
    def test_update_next_run_at_interval_never_ran(self):
        """Test that next_run_at = current time + interval."""
        # Update next_run_at
        PipelineScheduleService.update_next_run_at_for_pipeline(
            self.pipeline.id,
        )

        # Assert next_run_at is updated to last_run_at + interval
        schedule = PipelineScheduleService.fetch_schedule_for_pipeline(
            self.pipeline.id,
        )

        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'next_run_at',
            datetime.utcnow() + timedelta(seconds=int(schedule.schedule)),
        )

    def test_lock_schedule_for_pipeline(self):
        """Test that the schedule gets locked."""
        # Assert not locked
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'locked',
            False,
        )

        # Lock pipeline
        PipelineScheduleService.lock_schedule_for_pipeline(self.pipeline.id)

        # Assert locked
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'locked',
            True,
        )

    def test_unlock_schedule_for_pipeline(self):
        """Test that the schedule gets unlocked."""
        # Lock pipeline
        PipelineScheduleService.lock_schedule_for_pipeline(self.pipeline.id)

        # Assert locked
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'locked',
            True,
        )

        # Unlock pipeline
        PipelineScheduleService.unlock_schedule_for_pipeline(self.pipeline.id)

        # Assert unlocked
        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'locked',
            False,
        )

    def test_write_pipeline_schedule(self):
        """Test that we can write an entity to the repository."""
        entity = PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval)
        entity.schedule = '150'

        PipelineScheduleService.write_pipeline_schedule(entity)

        self._assert_pipeline_attribute_equals(
            self.pipeline.id,
            'schedule',
            '150',
        )

    def _assert_pipeline_attribute_equals(self, pipeline_id, attribute, expected):
        schedule = PipelineScheduleService.fetch_schedule_for_pipeline(
            pipeline_id,
        )

        self.assertEquals(
            getattr(schedule, attribute),
            expected,
        )
