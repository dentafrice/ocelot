from ocelot.services.entities.pipeline import PipelineEntity
from ocelot.services.mappers.pipeline import PipelineMapper
from ocelot.services.repositories.pipeline import PipelineRepository
from ocelot.tests import DatabaseTestCase


class TestPipelineRepository(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')

    def test_fetch_pipeline_by_id(self):
        """Test that a record can be retrieved from the datastore."""
        self.assertEquals(
            PipelineRepository.fetch_pipeline_by_id(self.pipeline.id),
            self.pipeline,
        )

    def test_write_record_new(self):
        """Test that we can create a new record."""
        entity = PipelineEntity.get_mock_object()

        PipelineRepository.write_record(
            PipelineMapper.to_record(entity)
        )

        pipeline = PipelineRepository.fetch_pipeline_by_id(entity.id)
        self.assertEquals(pipeline.name, entity.name)

    def test_write_record_update(self):
        """Test that we can write an updated record."""
        # Assert pipeline name is not 'new name'
        pipeline = PipelineRepository.fetch_pipeline_by_id(self.pipeline.id)
        self.assertNotEquals(pipeline.name, 'new name')

        # Update pipeline's name
        pipeline.name = 'new name'
        PipelineRepository.write_record(pipeline)

        # Pipeline's name should be 'new name'
        pipeline = PipelineRepository.fetch_pipeline_by_id(self.pipeline.id)
        self.assertEquals(pipeline.name, 'new name')
