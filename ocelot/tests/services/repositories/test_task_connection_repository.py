from ocelot.services.repositories.task_connection import TaskConnectionRepository
from ocelot.tests import TestCase

FAKE_PIPELINE_UUID = 'e6abe76b-4ce2-405c-a1f8-b42637d46035'
FAKE_PIPELINE2_UUID = '4dfd72b2-4158-45cf-a2e7-d5f94f969ded'

FAKE_RECORDS = {
    '1f2a02e8-658f-4fcf-a8fd-8ee0ad6766a0': {
        'to_task_id': '7fad2c37-1783-4917-b4ed-65ecb858068a',
        'from_task_id': '13652ea0-0125-4bff-b853-c6e2e9e9ce17',
        'pipeline_id': FAKE_PIPELINE_UUID,
    },

    '0b07f424-72d4-47f4-a643-7ca399acf8a5': {
        'to_task_id': '5b6840a7-63fd-48e5-84d1-6343634d4297',
        'from_task_id': 'd1841d93-a9f4-464e-8063-b174ed5e52eb',
        'pipeline_id': FAKE_PIPELINE2_UUID,
    },

    '7139b623-c91d-4e82-8a60-ba1daf2c9276': {
        'to_task_id': 'a09ae47b-27ad-4d8f-9735-a1b2e628d432',
        'from_task_id': 'f16db06d-4a0b-41c4-958c-f6a426b0e792',
        'pipeline_id': FAKE_PIPELINE_UUID,
    },
}


class TestTaskConnectionRepository(TestCase):
    def test_fetch_connections_for_pipeline(self):
        """Test that only connections for a provided pipeline are returned."""
        self.set_config('datastore.task_connections', FAKE_RECORDS)

        expected_record1 = {}
        expected_record1.update(FAKE_RECORDS['1f2a02e8-658f-4fcf-a8fd-8ee0ad6766a0'])
        expected_record1.update({'id': '1f2a02e8-658f-4fcf-a8fd-8ee0ad6766a0'})

        expected_record2 = {}
        expected_record2.update(FAKE_RECORDS['7139b623-c91d-4e82-8a60-ba1daf2c9276'])
        expected_record2.update({'id': '7139b623-c91d-4e82-8a60-ba1daf2c9276'})

        expected_records = [
            expected_record1,
            expected_record2,
        ]

        self.assertItemsEqual(
            TaskConnectionRepository.fetch_connections_for_pipeline(FAKE_PIPELINE_UUID),
            expected_records,
        )
