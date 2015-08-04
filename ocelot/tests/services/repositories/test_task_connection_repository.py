import uuid

from ocelot.services.entities.task_connection import TaskConnectionEntity
from ocelot.services.mappers.task_connection import TaskConnectionMapper
from ocelot.services.repositories.task_connection import TaskConnectionRepository
from ocelot.tests import DatabaseTestCase


class TestTaskConnectionRepository(DatabaseTestCase):
    def setUp(self):
        self.pipeline1 = self.install_fixture('pipeline')
        self.pipeline2 = self.install_fixture(
            'pipeline',
            overrides={
                'name': 'Second One,'
            }
        )

        self.connection1 = self.install_fixture('url_to_log_connection', overrides={
            'pipeline_id': self.pipeline1.id,
        })

        self.connection2 = self.install_fixture('url_to_log_connection', overrides={
            'pipeline_id': self.pipeline2.id,
        })

    def test_fetch_connections_for_pipeline(self):
        """Test that only connections for a provided pipeline are returned."""
        self.assertItemsEqual(
            TaskConnectionRepository.fetch_connections_for_pipeline(self.pipeline1.id),
            [
                self.connection1,
            ],
        )

    def test_write_record_new(self):
        """Test that we can create a new record."""
        entity = TaskConnectionEntity.get_mock_object()

        TaskConnectionRepository.write_record(
            TaskConnectionMapper.to_record(entity)
        )

        connections = TaskConnectionRepository.fetch_connections_for_pipeline(entity.pipeline_id)
        self.assertEquals(connections[0].id, entity.id)

    def test_write_record_update(self):
        """Test that we can write an updated record."""
        fake_uuid = uuid.uuid4()

        # Assert connection's from_task_id is not expected
        connection = TaskConnectionRepository.fetch_connections_for_pipeline(
            self.connection1.pipeline_id
        )[0]
        self.assertNotEquals(connection.from_task_id, fake_uuid)

        # Update connection's from_task_id
        connection.from_task_id = fake_uuid
        TaskConnectionRepository.write_record(connection)

        # Assert connection's from_task_id is as expected
        connection = TaskConnectionRepository.fetch_connections_for_pipeline(
            self.connection1.pipeline_id
        )[0]
        self.assertEquals(connection.from_task_id, fake_uuid)
