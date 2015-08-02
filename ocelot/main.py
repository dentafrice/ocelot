from ocelot.services import datastores
from ocelot.services.pipeline import PipelineService

if __name__ == '__main__':
    datastores.create_tables()
    datastores.initialize()

    PipelineService.run_pipeline_by_id(
        '96feda22-f80d-4cee-ad51-4e18de0b655a',
    )
