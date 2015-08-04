from ocelot.services.entities.pipeline import PipelineEntity
from ocelot.services.entities.pipeline_schedule import PipelineScheduleEntity
from ocelot.services.entities.task import TaskEntity
from ocelot.services.entities.task_connection import TaskConnectionEntity
from ocelot.services.pipeline import PipelineService
from ocelot.services.pipeline_schedule import PipelineScheduleService
from ocelot.services.task import TaskService
from ocelot.services.task_connection import TaskConnectionService


# BETA
class PipelineImportService(object):
    @classmethod
    def import_pipeline(cls, pipeline_data):
        if not pipeline_data.get('pipeline'):
            raise Exception('pipeline data is required')

        if not pipeline_data.get('pipeline_schedule'):
            raise Exception('pipeline schedule data is required')

        if not pipeline_data.get('tasks'):
            raise Exception('task data is required')

        if not pipeline_data.get('task_connections'):
            raise Exception('task connections are required')

        # Create Pipeline
        pipeline_entity = PipelineEntity(pipeline_data['pipeline'])
        pipeline_entity.validate()

        # Create PipelineSchedule
        pipeline_schedule_entity = PipelineScheduleEntity(pipeline_data['pipeline_schedule'])
        pipeline_schedule_entity.pipeline_id = pipeline_entity.id
        pipeline_schedule_entity.next_run_at = PipelineScheduleService.calculate_next_run_at_for_schedule(
            pipeline_schedule_entity
        )
        pipeline_schedule_entity.validate()

        # Create Tasks
        task_entities = []
        task_alias_to_id = {}

        for task_alias, task_data in pipeline_data['tasks'].items():
            task_entity = TaskEntity(task_data)
            task_entity.validate()

            task_entities.append(task_entity)
            task_alias_to_id[task_alias] = task_entity.id

        # Create TaskConnections
        task_connection_entities = []

        for from_alias, to_aliases in pipeline_data['task_connections'].items():
            from_task_id = task_alias_to_id[from_alias]

            for to_alias in to_aliases:
                to_task_id = task_alias_to_id[to_alias]

                task_connection_entity = TaskConnectionEntity({
                    'from_task_id': from_task_id,
                    'to_task_id': task_alias_to_id[to_alias],
                    'pipeline_id': pipeline_entity.id,
                })
                task_connection_entity.validate()

                task_connection_entities.append(task_connection_entity)

        # Save Pipeline
        PipelineService.write_pipeline(pipeline_entity)

        # Save PipelineSchedule (enabled = False)
        PipelineScheduleService.write_pipeline_schedule(pipeline_schedule_entity)

        # Save Tasks
        for task_entity in task_entities:
            TaskService.write_task(task_entity)

        # Save TaskConnections
        for task_connection_entity in task_connection_entities:
            TaskConnectionService.write_task_connection(task_connection_entity)
