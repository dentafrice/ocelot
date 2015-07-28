import copy

from ocelot import config


class TaskConnectionRepository(object):
    @classmethod
    def fetch_connections_for_pipeline(cls, pipeline_id):
        pipeline_id = str(pipeline_id)

        connections = config.get('datastore.task_connections').data

        matched_connections = []

        for connection_id, connection_data in connections.items():
            if connection_data['pipeline_id'] == pipeline_id:
                connection_data = copy.deepcopy(connection_data)
                connection_data['id'] = connection_id

                matched_connections.append(connection_data)

        return matched_connections
