from ocelot.services.mappers.pipeline_schedule import PipelineScheduleMapper
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleMapper(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline_schedule_cron')

    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            PipelineScheduleMapper.to_entity(self.pipeline_schedule_cron).to_native(),
            {
                'pipeline_id': self.pipeline_schedule_cron.pipeline_id,
                'schedule': self.pipeline_schedule_cron.schedule,
                'type': self.pipeline_schedule_cron.type,
                'next_run_at': self.pipeline_schedule_cron.next_run_at,
                'last_run_at': self.pipeline_schedule_cron.last_run_at,
                'locked': self.pipeline_schedule_cron.locked,
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = PipelineScheduleMapper.to_entity(self.pipeline_schedule_cron)
        record = PipelineScheduleMapper.to_record(entity)

        for c in record.__table__.columns:
            self.assertEquals(
                getattr(record, c.name),
                getattr(self.pipeline_schedule_cron, c.name),
            )
