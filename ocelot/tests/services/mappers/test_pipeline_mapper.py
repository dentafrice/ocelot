from ocelot.services.mappers.pipeline import PipelineMapper
from ocelot.tests import DatabaseTestCase


class TestPipelineMapper(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('pipeline')

    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            PipelineMapper.to_entity(self.pipeline).to_native(),
            {
                'id': self.pipeline.id,
                'name': self.pipeline.name,
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = PipelineMapper.to_entity(self.pipeline)

        self.assertEquals(
            PipelineMapper.to_record(entity).id,
            self.pipeline.id,
        )

        self.assertEquals(
            PipelineMapper.to_record(entity).name,
            self.pipeline.name,
        )
