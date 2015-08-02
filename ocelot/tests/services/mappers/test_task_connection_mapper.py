from ocelot.services.mappers.task_connection import TaskConnectionMapper
from ocelot.tests import DatabaseTestCase


class TestTaskConnectionMapper(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('url_to_log_connection')

    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            TaskConnectionMapper.to_entity(self.url_to_log_connection).to_native(),
            {
                'id': self.url_to_log_connection.id,
                'from_task_id': self.url_to_log_connection.from_task_id,
                'pipeline_id': self.url_to_log_connection.pipeline_id,
                'to_task_id': self.url_to_log_connection.to_task_id,
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = TaskConnectionMapper.to_entity(self.url_to_log_connection)
        record = TaskConnectionMapper.to_record(entity)

        for c in record.__table__.columns:
            self.assertEquals(
                getattr(record, c.name),
                getattr(self.url_to_log_connection, c.name),
            )
