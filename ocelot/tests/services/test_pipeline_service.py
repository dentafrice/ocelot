import mock
import uuid

from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.services.pipeline import (
    PipelineRepository,
    PipelineService,
    TaskConnectionService,
    TaskService,
)
from ocelot.tests import DatabaseTestCase


class TestPipelineService(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')

    @mock.patch.object(PipelineRepository, 'fetch_pipeline_by_id')
    def test_fetch_pipeline_by_id(self, mock_fetch):
        """Test that you can fetch a PipelineEntity by ID."""
        mock_fetch.return_value = self.pipeline

        entity = PipelineService.fetch_pipeline_by_id(self.pipeline.id)

        self.assertEquals(
            entity.id,
            self.pipeline.id,
        )

    @mock.patch.object(TaskService, 'process_task_with_data')
    @mock.patch.object(TaskConnectionService, 'build_graph_for_pipeline')
    def test_run_pipeline_by_id(self, mock_graph, mock_process):
        node1_uuid = uuid.UUID('8bce531f-1c75-4526-b584-62a9e716933f')
        node2_uuid = uuid.UUID('de1b8346-0a26-4aad-b245-bb5cabf0daed')
        node3_uuid = uuid.UUID('cd227069-66cc-4ed3-8112-1cb2e85c4917')

        mock_graph.return_value = {
            'graph': {
                node1_uuid: set([
                    node2_uuid,
                ]),

                node2_uuid: set([
                    node3_uuid,
                ]),
            },

            'source_ids': [
                node1_uuid,
            ],
        }

        mock_process.side_effect = [
            'fake_response1',
            'fake_response2',
            None,  # last output doesn't return anything
        ]

        PipelineService.run_pipeline_by_id(self.pipeline.id)

        mock_graph.assert_called_once_with(self.pipeline.id)

        self.assertEquals(mock_process.call_count, 3)

        # node1.process
        self.assertEquals(
            mock_process.call_args_list[0][0],
            (node1_uuid, None),
        )

        # node2.process
        self.assertEquals(
            mock_process.call_args_list[1][0],
            (node2_uuid, 'fake_response1'),
        )

        # node3.process
        self.assertEquals(
            mock_process.call_args_list[2][0],
            (node3_uuid, 'fake_response2'),
        )

    @mock.patch.object(TaskService, 'process_task_with_data')
    @mock.patch.object(TaskConnectionService, 'build_graph_for_pipeline')
    def test_stop_processing_exception_only_stops_one_path(
        self,
        mock_graph,
        mock_process,
    ):
        """Test that if a StopProcessingException is encountered
        that it only stops one path.

        Given:
        A ->
            B ->
                C
            D ->
                E

        If B raises a `StopProcessingException`, D and E should
        still be called but C should not.
        """
        a = uuid.UUID('a722396f-8890-438c-a553-408b494491e9')
        b = uuid.UUID('45e81c1a-361a-4276-9df7-29cea6b0f6f2')
        c = uuid.UUID('8c55b14b-75d4-4e6e-a7c9-a1e325279d77')
        d = uuid.UUID('ec7b034f-2ab1-45b4-8da4-c12db71191bc')
        e = uuid.UUID('d8c8b029-5ca7-4602-95b9-af720de934e8')

        graph = {
            'graph': {
                a: set([
                    b,
                    d,
                ]),

                b: set([
                    c,
                ]),

                d: set([
                    e,
                ])
            },

            'source_ids': [
                a,
            ],
        }

        def fake_process(task_id, data):
            if task_id == a:
                return 'a_response'
            elif task_id == b:
                raise StopProcessingException
            elif task_id == d:
                return 'd_response'
            elif task_id == e:
                return None  # last doesn't return anything

        mock_process.side_effect = fake_process
        mock_graph.return_value = graph

        PipelineService.run_pipeline_by_id(self.pipeline.id)

        self.assertEquals(mock_process.call_count, 4)

        # a.process
        self.assertEquals(
            mock_process.call_args_list[0][0],
            (a, None),
        )

        # b.process
        self.assertEquals(
            mock_process.call_args_list[1][0],
            (b, 'a_response'),
        )

        # d.process
        self.assertEquals(
            mock_process.call_args_list[2][0],
            (d, 'a_response'),
        )

        # e.process
        self.assertEquals(
            mock_process.call_args_list[3][0],
            (e, 'd_response'),
        )
