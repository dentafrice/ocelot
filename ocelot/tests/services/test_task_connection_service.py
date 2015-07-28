import mock
import uuid

from ocelot.services.task_connection import (
    TaskConnectionRepository,
    TaskConnectionService,
)
from ocelot.tests import TestCase

FAKE_PIPELINE_UUID = '62b35dbf-3866-4943-b46a-902639022f27'
FAKE_RECORD1 = {
    'id': '1680f422-30cb-4344-9143-96c479cdb2ee',
    'from_task_id': '73102523-5492-497b-9cbd-fc34a7749753',
    'to_task_id': '23e68d83-0eb4-456e-b85d-c82c78009ff4',
    'pipeline_id': FAKE_PIPELINE_UUID,
}

FAKE_RECORD2 = {
    'id': '3587386f-f824-49c5-ac2c-3a33257a9a4c',
    'from_task_id': '23e68d83-0eb4-456e-b85d-c82c78009ff4',
    'to_task_id': 'b4af7ed9-2562-41ac-8a58-ba1d5ec14feb',
    'pipeline_id': FAKE_PIPELINE_UUID,
}


class TestTaskConnectionService(TestCase):
    @mock.patch.object(TaskConnectionRepository, 'fetch_connections_for_pipeline')
    def test_fetch_task_connections_for_pipeline(self, mock_fetch):
        """Test that a list of TaskConnectionEntities is returned."""
        mock_fetch.return_value = [FAKE_RECORD1, FAKE_RECORD2]

        entities = TaskConnectionService.fetch_task_connections_for_pipeline(FAKE_PIPELINE_UUID)
        self.assertEqual(str(entities[0].id), FAKE_RECORD1['id'])

    @mock.patch.object(TaskConnectionRepository, 'fetch_connections_for_pipeline')
    def test_build_graph_for_pipeline(self, mock_fetch):
        """Test that a graph is returned when given a pipeline id."""
        mock_fetch.return_value = [FAKE_RECORD1, FAKE_RECORD2]

        self.assertEquals(
            TaskConnectionService.build_graph_for_pipeline(FAKE_PIPELINE_UUID),
            {
                'graph': {
                    uuid.UUID(FAKE_RECORD1['from_task_id']): set([
                        uuid.UUID(FAKE_RECORD1['to_task_id']),
                    ]),

                    uuid.UUID(FAKE_RECORD2['from_task_id']): set([
                        uuid.UUID(FAKE_RECORD2['to_task_id']),
                    ]),
                },

                'source_ids': [
                    uuid.UUID(FAKE_RECORD1['from_task_id']),
                ],
            },
        )
