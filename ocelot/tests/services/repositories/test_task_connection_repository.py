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
