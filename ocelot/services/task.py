from ocelot.lib import logging

from ocelot.services.constants.task import TASK_MAP
from ocelot.services.mappers.task import TaskMapper
from ocelot.services.repositories.task import TaskRepository

log = logging.getLogger('ocelot.tasks')


class TaskService(object):
    @classmethod
    def fetch_task_by_id(cls, id):
        """Fetch TaskEntity by id.

        :param str id:
        :returns TaskEntity:
        """
        return TaskMapper.to_entity(
            TaskRepository.fetch_task_by_id(id),
        )

    @classmethod
    def process_task_with_data(cls, id, data):
        """Instantiates and runs task by ID.

        :param str id:
        :param object data:
        :returns object: response from task class
        """
        task_entity = cls.fetch_task_by_id(id)

        log.info('Running task: {}:{}'.format(task_entity.type, id))

        task_class = TASK_MAP[task_entity.type](
            id=task_entity.id,
            **task_entity.config
        )

        return task_class.process(data)

    @classmethod
    def write_task(cls, task):
        """Writes TaskEntity to the repository.

        :param TaskEntity task:
        """
        task.validate()

        TaskRepository.write_record(
            TaskMapper.to_record(task),
        )
