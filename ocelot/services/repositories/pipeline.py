from ocelot.services.datastores import PipelineStore, Session
from ocelot.services.repositories import utils


class PipelineRepository(object):
    @classmethod
    @utils.handle_no_result_found
    def fetch_pipeline_by_id(cls, id):
        """Returns pipeline record by id.

        :param str id:
        :returns TaskStore: record
        """
        return (
            Session.query(PipelineStore)
            .filter(PipelineStore.id == id)
            .one()
        )
