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
        self.install_fixture('pipeline_schedule_cron')
        self.install_fixture('pipeline_schedule_interval')

    @mock.patch.object(PipelineScheduleRepository, 'fetch_schedules_for_pipeline')
    def test_fetch_schedules_for_pipeline(self, mock_fetch):
        """Test that you can fetch schedules for a pipeline."""
        mock_fetch.return_value = [
            self.pipeline_schedule_cron,
            self.pipeline_schedule_interval,
        ]

        self.assertEqual(
            PipelineScheduleService.fetch_schedules_for_pipeline(self.pipeline.id),
            [
                PipelineScheduleMapper.to_entity(self.pipeline_schedule_cron),
                PipelineScheduleMapper.to_entity(self.pipeline_schedule_interval),
            ],
        )
