from collections import deque

from ocelot.lib import logging
from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.services.pipeline_schedule import PipelineScheduleService
from ocelot.services.task import TaskService
from ocelot.services.task_connection import TaskConnectionService
from ocelot.services.mappers.pipeline import PipelineMapper
from ocelot.services.repositories.pipeline import PipelineRepository

log = logging.getLogger('ocelot.pipelines')


class PipelineService(object):
    @classmethod
    def fetch_pipeline_by_id(cls, id):
        """Returns PipelineEntity by id.

        :param str id:
        :returns PipelineEntity:
        """
        return PipelineMapper.to_entity(
            PipelineRepository.fetch_pipeline_by_id(id),
        )

    @classmethod
    def run_pipeline_by_id(cls, id):
        """Runs a pipeline by id.

        :param str id:
        """
        log.info('Running pipeline: {}'.format(id))

        PipelineScheduleService.pre_run_schedule(id)

        # get graph
        graph_data = TaskConnectionService.build_graph_for_pipeline(id)

        # process graph
        queue = deque()

        for source_id in graph_data['source_ids']:
            queue.appendleft((source_id, None))

        while len(queue):
            task_id, data = queue.pop()

            try:
                task_response = TaskService.process_task_with_data(task_id, data)

                try:
                    for next_id in graph_data['graph'][task_id]:
                        queue.appendleft((next_id, task_response))
                except KeyError:
                    # end of list
                    pass
            except StopProcessingException:
                pass

        PipelineScheduleService.post_run_schedule(id)

    @classmethod
    def write_pipeline(cls, pipeline_entity):
        """Writes a PipelineEntity to the database.

        :param PipelineEntity pipeline_entity:
        """
        pipeline_entity.validate()

        PipelineRepository.write_record(
            PipelineMapper.to_record(pipeline_entity)
        )
