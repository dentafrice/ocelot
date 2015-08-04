from ocelot.services.datastores import TaskStore, Session
from ocelot.services.repositories import utils


class TaskRepository(object):
    @classmethod
    @utils.handle_no_result_found
    def fetch_task_by_id(cls, id):
        """Fetches task record by id.

        :param str id:
        :returns TaskStore: record
        """
        return (
            Session.query(TaskStore)
            .filter(TaskStore.id == id)
            .one()
        )

    @classmethod
    def write_record(cls, record):
        """Writes a record to the database.

        :param TaskStore record:
        """
        Session.merge(record)
        Session.commit()
