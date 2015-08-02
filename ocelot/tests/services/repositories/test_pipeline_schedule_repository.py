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
