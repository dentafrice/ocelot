from ocelot.services.datastores import PipelineStore, Session
from ocelot.services.repositories import utils


class PipelineRepository(object):
    @classmethod
    @utils.handle_no_result_found
    def fetch_pipeline_by_id(cls, id):
        """Returns pipeline record by id.

        :param str id:
        :returns PipelineStore: record
        """
        return (
            Session.query(PipelineStore)
            .filter(PipelineStore.id == id)
            .one()
        )

    @classmethod
    def write_record(cls, record):
        """Writes a record to the database.

        :param PipelineStore record:
        """
        Session.merge(record)
        Session.commit()
