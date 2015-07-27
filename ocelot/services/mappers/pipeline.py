from ocelot.services.entities.pipeline import PipelineEntity


class PipelineMapper(object):
    @staticmethod
    def to_entity(record):
        """Converts record into a PipelineEntity.

        :param dict record:
        :returns PipelineEntity:
        """
        return PipelineEntity({
            'id': record['id'],
            'name': record['name'],
        })

    @staticmethod
    def to_record(entity):
        """Converts PipelineEntity into a record.

        :param PipelineEntity entity:
        :returns dict: record
        """
        return entity.to_native()
