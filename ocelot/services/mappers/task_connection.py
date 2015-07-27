from ocelot.services.entities.task_connection import TaskConnectionEntity


class TaskConnectionMapper(object):
    @staticmethod
    def to_entity(record):
        """Converts record into a TaskConnectionEntity.

        :param dict record:
        :returns TaskConnectionEntity:
        """
        return TaskConnectionEntity({
            'id': record['id'],
            'from_task_id': record['from_task_id'],
            'pipeline_id': record['pipeline_id'],
            'to_task_id': record['to_task_id'],
        })

    @staticmethod
    def to_record(entity):
        """Converts TaskConnectionEntity into a record.

        :param TaskConnectionEntity entity:
        :returns dict: record
        """
        return entity.to_native()
