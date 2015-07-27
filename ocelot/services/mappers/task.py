from ocelot.services.entities.task import TaskEntity


class TaskMapper(object):
    @staticmethod
    def to_entity(record):
        return TaskEntity({
            'id': record['id'],
            'type': record['type'],
            'config': record['config'],
        })

    @staticmethod
    def to_record(entity):
        return entity.to_native()
