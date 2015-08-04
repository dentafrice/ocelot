from ocelot.services.entities.task import TaskEntity
from ocelot.services.mappers.task import TaskMapper
from ocelot.services.repositories.task import TaskRepository
from ocelot.tests import DatabaseTestCase


class TestTaskRepository(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('url_task')

    def test_fetch_task_by_id(self):
        """Test that a record can be retrieved from the datastore."""
        self.assertEquals(
            TaskRepository.fetch_task_by_id(self.url_task.id),
            self.url_task,
        )

    def test_write_record_new(self):
        """Test that we can create a new record."""
        entity = TaskEntity.get_mock_object()

        TaskRepository.write_record(
            TaskMapper.to_record(entity)
        )

        task = TaskRepository.fetch_task_by_id(entity.id)
        self.assertEquals(task.id, entity.id)

    def test_write_record_update(self):
        """Test that we can write an updated record."""
        # Assert task's config is not expected
        task = TaskRepository.fetch_task_by_id(self.url_task.id)
        self.assertNotEquals(task.config, {'url': 'hey'})

        # Update tasks's config
        task.config = {'url': 'hey'}
        TaskRepository.write_record(task)

        # Assert tasks' config is as expected
        task = TaskRepository.fetch_task_by_id(self.url_task.id)
        self.assertEquals(task.config, {'url': 'hey'})
