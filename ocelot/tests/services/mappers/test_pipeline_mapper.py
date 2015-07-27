import uuid

from ocelot.services.mappers.pipeline import PipelineMapper
from ocelot.tests import TestCase

FAKE_RECORD = {
    'id': 'b9d1410d-4111-4771-b321-7ff28620cc15',
    'name': 'Cool Pipeline',
}


class TestPipelineMapper(TestCase):
    def test_to_entity(self):
        """Test that a record can be converted into an entity."""

        self.assertEquals(
            PipelineMapper.to_entity(FAKE_RECORD).to_native(),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'name': FAKE_RECORD['name'],
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = PipelineMapper.to_entity(FAKE_RECORD)

        self.assertEquals(
            PipelineMapper.to_record(entity),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'name': FAKE_RECORD['name'],
            }
        )
