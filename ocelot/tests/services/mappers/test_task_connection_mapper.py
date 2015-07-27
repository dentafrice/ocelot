import uuid

from ocelot.services.mappers.task_connection import TaskConnectionMapper
from ocelot.tests import TestCase

FAKE_RECORD = {
    'id': '4f33bb64-d815-482c-8527-7ee596b5fd26',
    'from_task_id': '32d48ae6-3dd6-4cdc-9eb6-130ad3f4818d',
    'pipeline_id': 'd8b098bc-5e15-4901-8e34-a4e66905c2c8',
    'to_task_id': '19c3c5c4-a87a-4ccb-ad3f-3cdf0c68eaed',
}


class TestTaskConnectionMapper(TestCase):
    def test_to_entity(self):
        """Test that a record can be converted into an entity."""
        self.assertEquals(
            TaskConnectionMapper.to_entity(FAKE_RECORD).to_native(),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'from_task_id': uuid.UUID(FAKE_RECORD['from_task_id']),
                'pipeline_id': uuid.UUID(FAKE_RECORD['pipeline_id']),
                'to_task_id': uuid.UUID(FAKE_RECORD['to_task_id']),
            }
        )

    def test_to_record(self):
        """Test that an entity can be converted into a record."""
        entity = TaskConnectionMapper.to_entity(FAKE_RECORD)

        self.assertEquals(
            TaskConnectionMapper.to_record(entity),
            {
                'id': uuid.UUID(FAKE_RECORD['id']),
                'from_task_id': uuid.UUID(FAKE_RECORD['from_task_id']),
                'pipeline_id': uuid.UUID(FAKE_RECORD['pipeline_id']),
                'to_task_id': uuid.UUID(FAKE_RECORD['to_task_id']),
            }
        )
