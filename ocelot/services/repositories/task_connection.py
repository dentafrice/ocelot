from ocelot.services.datastores import TaskConnectionStore, Session


class TaskConnectionRepository(object):
    @classmethod
    def fetch_connections_for_pipeline(cls, pipeline_id):
        """Fetches list of task connections for a pipeline id.

        :param str pipeline_id:
        :returns list: list of task connection records (dict)
        """
        return (
            Session.query(TaskConnectionStore)
            .filter(TaskConnectionStore.pipeline_id == pipeline_id)
        ).all()
