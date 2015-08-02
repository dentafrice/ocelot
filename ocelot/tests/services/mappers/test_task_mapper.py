from ocelot.services.mappers.task import TaskMapper
from ocelot.tests import DatabaseTestCase


class TestTaskMapper(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('url_task')

    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            TaskMapper.to_entity(self.url_task).to_native(),
            {
                'id': self.url_task.id,
                'type': self.url_task.type,
                'config': self.url_task.config,
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = TaskMapper.to_entity(self.url_task)
        record = TaskMapper.to_record(entity)

        for c in record.__table__.columns:
            self.assertEquals(
                getattr(record, c.name),
                getattr(self.url_task, c.name)
            )
