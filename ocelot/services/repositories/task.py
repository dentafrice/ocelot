import copy

from ocelot import config
from ocelot.services.exceptions import ResourceNotFoundException


class TaskRepository(object):
    @classmethod
    def fetch_task_by_id(cls, id):
        id = str(id)

        tasks = config.get('datastore.tasks').data

        try:
            task_data = copy.deepcopy(tasks[id])
            task_data['id'] = id

            return task_data
        except KeyError:
            raise ResourceNotFoundException
