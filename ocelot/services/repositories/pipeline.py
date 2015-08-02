from ocelot.services.datastores import NoResultFound, PipelineStore, Session
from ocelot.services.exceptions import ResourceNotFoundException


class PipelineRepository(object):
    @classmethod
    def fetch_pipeline_by_id(cls, id):
        """Returns pipeline record by id.

        :param str id:
        :returns TaskStore: record
        """
        try:
            return (
                Session.query(PipelineStore)
                .filter(PipelineStore.id == id)
                .one()
            )
        except NoResultFound:
            raise ResourceNotFoundException
