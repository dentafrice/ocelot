from ocelot.services.datastores import NoResultFound, TaskStore, Session
from ocelot.services.exceptions import ResourceNotFoundException


class TaskRepository(object):
    @classmethod
    def fetch_task_by_id(cls, id):
        """Fetches task record by id.

        :param str id:
        :returns TaskStore: record
        """
        try:
            return (
                Session.query(TaskStore)
                .filter(TaskStore.id == id)
                .one()
            )
        except NoResultFound:
            raise ResourceNotFoundException
