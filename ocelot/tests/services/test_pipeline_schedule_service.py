import mock

from ocelot.services.pipeline_schedule import (
    PipelineScheduleMapper,
    PipelineScheduleRepository,
    PipelineScheduleService,
)
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleService(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')
        self.install_fixture('pipeline_schedule_interval')

    @mock.patch.object(PipelineScheduleRepository, 'fetch_schedule_for_pipeline')
    def test_fetch_schedule_for_pipeline(self, mock_fetch):
        """Test that you can fetch schedules for a pipeline."""
        mock_fetch.return_value = self.pipeline_schedule_interval

        self.assertEqual(
            PipelineScheduleService.fetch_schedule_for_pipeline(self.pipeline.id),
            PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval),
        )

    @mock.patch.object(PipelineScheduleRepository, 'fetch_schedules_to_run')
    def test_fetch_schedules_to_run(self, mock_fetch):
        """Test that schedules that need to run are returned."""
        mock_fetch.return_value = [
            self.pipeline_schedule_interval,
        ]

        self.assertEqual(
            PipelineScheduleService.fetch_schedules_to_run(),
            [
                PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval),
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

    @mock.patch.object(PipelineScheduleService, 'update_schedule_for_pipeline')
    def test_lock_schedule_for_pipeline(self, mock_update):
        """Test that the schedule gets locked."""
        PipelineScheduleService.lock_schedule_for_pipeline(self.pipeline.id)
        mock_update.assert_called_once_with(
            self.pipeline.id,
            {'locked': True},
        )

    @mock.patch.object(PipelineScheduleService, 'update_schedule_for_pipeline')
    def test_unlock_schedule_for_pipeline(self, mock_update):
        """Test that the schedule gets unlocked."""
        PipelineScheduleService.unlock_schedule_for_pipeline(self.pipeline.id)
        mock_update.assert_called_once_with(
            self.pipeline.id,
            {'locked': False},
        )

    def test_update_schedule_for_pipeline(self):
        """Test that the schedule gets updated with the requested attributes."""
        schedule = PipelineScheduleService.fetch_schedule_for_pipeline(self.pipeline.id)
        self.assertFalse(schedule.locked)
        self.assertNotEquals(schedule.schedule, '20')

        PipelineScheduleService.update_schedule_for_pipeline(
            self.pipeline.id,
            {
                'locked': True,
                'schedule': '20',
            },
        )

        schedule = PipelineScheduleService.fetch_schedule_for_pipeline(self.pipeline.id)
        self.assertTrue(schedule.locked)
        self.assertEquals(schedule.schedule, '20')

    @mock.patch.object(PipelineScheduleRepository, 'write_record')
    def test_write_pipeline_schedule(self, mock_write_record):
        """Test that we can write an entity to the repository."""
        entity = PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval)
        entity.schedule = '150'

        PipelineScheduleService.write_pipeline_schedule(entity)

        self.assertTrue(mock_write_record.called)
        record = mock_write_record.call_args[0][0]
        self.assertEquals(record.schedule, '150')
