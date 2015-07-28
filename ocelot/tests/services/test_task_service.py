import mock

from ocelot.services.task import (
    TaskRepository,
    TaskService,
)
from ocelot.tests import TestCase

FAKE_RECORD = {
    'id': 'e588ec7e-fb47-4770-99dd-3865d8a127df',
    'type': 'URLInput',
    'config': {
        'url': 'http://google.com',
    }
}


class TestTaskService(TestCase):
    @mock.patch.object(TaskRepository, 'fetch_task_by_id')
    def test_fetch_task_by_id(self, mock_fetch):
        """Test that the correct TaskEntity is returned."""
        mock_fetch.return_value = FAKE_RECORD

        entity = TaskService.fetch_task_by_id(FAKE_RECORD['id'])

        self.assertEquals(str(entity.id), FAKE_RECORD['id'])

    @mock.patch.object(TaskRepository, 'fetch_task_by_id')
    @mock.patch('ocelot.pipeline.tasks.inputs.URLInput.process')
    def test_process_task_with_data(self, mock_process, mock_fetch):
        """Test that the right task class is created and called."""
        mock_fetch.return_value = FAKE_RECORD

        TaskService.process_task_with_data(FAKE_RECORD['id'], 'fake_data')
        mock_process.assert_called_once_with('fake_data')
