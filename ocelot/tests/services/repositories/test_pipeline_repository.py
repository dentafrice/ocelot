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
