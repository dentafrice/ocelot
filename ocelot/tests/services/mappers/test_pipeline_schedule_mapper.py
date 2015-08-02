from ocelot.services.mappers.pipeline_schedule import PipelineScheduleMapper
from ocelot.tests import DatabaseTestCase


class TestPipelineScheduleMapper(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline_schedule')

    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            PipelineScheduleMapper.to_entity(self.pipeline_schedule).to_native(),
            {
                'id': self.pipeline_schedule.id,
                'pipeline_id': self.pipeline_schedule.pipeline_id,
                'schedule': self.pipeline_schedule.schedule,
                'schedule_type': self.pipeline_schedule.schedule_type,
                'next_run_at': self.pipeline_schedule.next_run_at,
                'last_run_at': self.pipeline_schedule.last_run_at,
                'locked': self.pipeline_schedule.locked,
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = PipelineScheduleMapper.to_entity(self.pipeline_schedule)
        record = PipelineScheduleMapper.to_record(entity)

        for c in record.__table__.columns:
            self.assertEquals(
                getattr(record, c.name),
                getattr(self.pipeline_schedule, c.name),
            )
