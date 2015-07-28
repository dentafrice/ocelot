import copy

from ocelot import config
from ocelot.services.exceptions import ResourceNotFoundException


class PipelineRepository(object):
    @classmethod
    def fetch_pipeline_by_id(cls, id):
        id = str(id)

        pipelines = config.get('datastore.pipelines').data

        try:
            pipeline_data = copy.deepcopy(pipelines[id])
            pipeline_data['id'] = id

            return pipeline_data
        except KeyError:
            raise ResourceNotFoundException
