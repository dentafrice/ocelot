from ocelot.services.repositories.pipeline_schedule import PipelineScheduleRepository
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleRepository(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')
        self.install_fixture('pipeline_schedule_cron')
        self.install_fixture('pipeline_schedule_interval')

    def test_fetch_schedules_for_pipeline(self):
        """Test that schedules can be fetched for a pipeline."""
        self.assertItemsEqual(
            PipelineScheduleRepository.fetch_schedules_for_pipeline(self.pipeline.id),

            [
                self.pipeline_schedule_cron,
                self.pipeline_schedule_interval,
            ],
        )

    def test_write_record(self):
        """Test that we can write a record to the database."""
        def fetch_record(id):
            return filter(
                lambda r: r.id == id,
                PipelineScheduleRepository.fetch_schedules_for_pipeline(self.pipeline.id),
            )[0]

        record = self.pipeline_schedule_interval

        self.assertNotEquals(
            fetch_record(record.id).schedule,
            '150',
        )

        record.schedule = '150'
        PipelineScheduleRepository.write_record(record)

        self.assertEquals(
            fetch_record(record.id).schedule,
            '150',
        )
