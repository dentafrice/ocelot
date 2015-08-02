import mock

from ocelot.services.task_connection import (
    TaskConnectionRepository,
    TaskConnectionService,
)
from ocelot.tests import DatabaseTestCase


class TestTaskConnectionService(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')
        self.install_fixture('url_to_log_connection')
        self.install_fixture('raw_input_to_log_connection')

    @mock.patch.object(TaskConnectionRepository, 'fetch_connections_for_pipeline')
    def test_fetch_task_connections_for_pipeline(self, mock_fetch):
        """Test that a list of TaskConnectionEntities is returned."""
        mock_fetch.return_value = [
            self.url_to_log_connection,
            self.raw_input_to_log_connection,
        ]

        entities = TaskConnectionService.fetch_task_connections_for_pipeline(self.pipeline.id)
        self.assertEqual(entities[0].id, self.url_to_log_connection.id)

    @mock.patch.object(TaskConnectionRepository, 'fetch_connections_for_pipeline')
    def test_build_graph_for_pipeline(self, mock_fetch):
        """Test that a graph is returned when given a pipeline id."""
        mock_fetch.return_value = [
            self.url_to_log_connection,
            self.raw_input_to_log_connection,
        ]

        graph_data = TaskConnectionService.build_graph_for_pipeline(self.pipeline.id)

        self.assertEquals(graph_data['graph'], {
            self.url_to_log_connection.from_task_id: set([
                self.url_to_log_connection.to_task_id,
            ]),

            self.raw_input_to_log_connection.from_task_id: set([
                self.raw_input_to_log_connection.to_task_id,
            ])
        })

        self.assertItemsEqual(graph_data['source_ids'], [
            self.raw_input_to_log_connection.from_task_id,
            self.url_to_log_connection.from_task_id,
        ])
