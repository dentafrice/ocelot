import mock

from ocelot.services.entities.task import TaskEntity
from ocelot.services.exceptions import ResourceNotFoundException
from ocelot.services.task import (
    TaskRepository,
    TaskService,
)
from ocelot.tests import DatabaseTestCase


class TestTaskService(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('url_task')

    @mock.patch.object(TaskRepository, 'fetch_task_by_id')
    def test_fetch_task_by_id(self, mock_fetch):
        """Test that the correct TaskEntity is returned."""
        mock_fetch.return_value = self.url_task

        entity = TaskService.fetch_task_by_id(self.url_task.id)

        self.assertEquals(entity.id, self.url_task.id)

    @mock.patch.object(TaskRepository, 'fetch_task_by_id')
    @mock.patch('ocelot.services.constants.task.URLInput.process')
    def test_process_task_with_data(self, mock_process, mock_fetch):
        """Test that the right task class is created and called."""
        mock_fetch.return_value = self.url_task

        TaskService.process_task_with_data(self.url_task.id, 'fake_data')
        mock_process.assert_called_once_with('fake_data')

    def test_write_task(self):
        """Test that the provided entity gets written to the repository."""
        entity = TaskEntity.get_mock_object()

        with self.assertRaises(ResourceNotFoundException):
            TaskService.fetch_task_by_id(entity.id)

        TaskService.write_task(entity)

        self.assertEquals(
            TaskService.fetch_task_by_id(entity.id),
            entity,
        )
