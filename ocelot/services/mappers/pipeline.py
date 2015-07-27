from ocelot.services.entities.pipeline import PipelineEntity


class PipelineMapper(object):
    @staticmethod
    def to_entity(record):
        return PipelineEntity({
            'id': record['id'],
            'name': record['name'],
        })

    @staticmethod
    def to_record(entity):
        return entity.to_native()
