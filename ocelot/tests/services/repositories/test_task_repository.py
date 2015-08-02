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
