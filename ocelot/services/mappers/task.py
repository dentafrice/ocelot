from ocelot.services.entities.task import TaskEntity


class TaskMapper(object):
    @staticmethod
    def to_entity(record):
        """Converts record into a TaskEntity.

        :param dict record:
        :returns TaskEntity:
        """
        return TaskEntity({
            'id': record['id'],
            'type': record['type'],
            'config': record['config'],
        })

    @staticmethod
    def to_record(entity):
        """Converts TaskEntity into a record.

        :param TaskEntity entity:
        :returns dict: record
        """
        return entity.to_native()
