from ocelot.services import datastores
from ocelot.services.pipeline import PipelineService

if __name__ == '__main__':
    datastores.create_tables()
    datastores.initialize()

    # XKCD
    #  PipelineService.run_pipeline_by_id(
    #      '9aa97f4e-387d-4d06-ac00-f4fc344514da',
    #  )

    # Taraval
    PipelineService.run_pipeline_by_id(
        '86b48bf6-6e55-4a2e-991a-9c15f1f77b80',
    )
