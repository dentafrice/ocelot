from ocelot.services.mappers.task_connection import TaskConnectionMapper
from ocelot.services.repositories.task_connection import TaskConnectionRepository


class TaskConnectionService(object):
    @classmethod
    def fetch_task_connections_for_pipeline(cls, pipeline_id):
        """Returns list of TaskConnectionEntities for a pipeline.

        :param str pipeline_id:
        :returns list: TaskConnectionEntities
        """
        return map(
            TaskConnectionMapper.to_entity,
            TaskConnectionRepository.fetch_connections_for_pipeline(pipeline_id),
        )

    @classmethod
    def build_graph_for_pipeline(cls, pipeline_id):
        """Builds graph for a pipeline id.

        :param str pipeline_id:
        :returns dict:
            graph: dict of task_id => list of output task ids
            source_ids: list of task_ids that contain no inputs
        """
        connections = cls.fetch_task_connections_for_pipeline(pipeline_id)

        graph_from_to = {}
        graph_to_from = {}

        for connection in connections:
            from_task_id = connection.from_task_id
            to_task_id = connection.to_task_id

            graph_from_to.setdefault(from_task_id, set())
            graph_to_from.setdefault(to_task_id, set())

            graph_from_to[from_task_id].add(to_task_id)
            graph_to_from[to_task_id].add(from_task_id)

        source_ids = set(graph_from_to.keys()) - set(graph_to_from.keys())

        return {
            'graph': graph_from_to,
            'source_ids': list(source_ids),
        }
