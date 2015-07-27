import uuid

from ocelot.services.mappers.task import TaskMapper
from ocelot.tests import TestCase

FAKE_RECORD = {
    'id': '9402fd61-4f92-4c8a-a420-add97c09f261',
    'type': 'URLInput',
    'config': {
        'url': 'http://example.com/'
    }
}


class TestTaskMapper(TestCase):
    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            TaskMapper.to_entity(FAKE_RECORD).to_native(),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'type': FAKE_RECORD['type'],
                'config': FAKE_RECORD['config'],
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = TaskMapper.to_entity(FAKE_RECORD)

        self.assertEquals(
            TaskMapper.to_record(entity),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'type': FAKE_RECORD['type'],
                'config': FAKE_RECORD['config'],
            }
        )
