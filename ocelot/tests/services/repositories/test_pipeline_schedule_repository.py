from datetime import datetime, timedelta

from ocelot.services.repositories.pipeline_schedule import PipelineScheduleRepository
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleRepository(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')
        self.install_fixture('pipeline_schedule_interval')

    def test_fetch_schedule_for_pipeline(self):
        """Test that a schedule can be fetched for a pipeline."""
        self.assertEqual(
            PipelineScheduleRepository.fetch_schedule_for_pipeline(self.pipeline.id),
            self.pipeline_schedule_interval,
        )

    def test_fetch_schedules_to_run(self):
        """Test that schedules that need to run (next_run_at <= now) are returned."""
        self.assertEqual(
            PipelineScheduleRepository.fetch_schedules_to_run(),
            [
                self.pipeline_schedule_interval,
            ]
        )

    def test_fetch_schedules_later(self):
        """Test that schedules that do not need to run (next_run_at > now) are not returned."""
        self.uninstall_fixture('pipeline_schedule_interval')
        self.install_fixture('pipeline_schedule_interval', overrides={
            'next_run_at': datetime.utcnow() + timedelta(hours=6),
        })

        self.assertEqual(
            PipelineScheduleRepository.fetch_schedules_to_run(),
            [],
        )

    def test_fetch_schedules_to_run_locked(self):
        """Test that locked schedules are not returned."""
        self.uninstall_fixture('pipeline_schedule_interval')
        self.install_fixture('pipeline_schedule_interval', overrides={
            'locked': True,
        })

        self.assertEqual(
            PipelineScheduleRepository.fetch_schedules_to_run(),
            [],
        )

    def test_write_record(self):
        """Test that we can write a record to the database."""
        self.assertNotEquals(
            PipelineScheduleRepository.fetch_schedule_for_pipeline(self.pipeline.id).schedule,
            '150',
        )

        record = self.pipeline_schedule_interval
        record.schedule = '150'
        PipelineScheduleRepository.write_record(record)

        self.assertEquals(
            PipelineScheduleRepository.fetch_schedule_for_pipeline(self.pipeline.id).schedule,
            '150',
        )
