from ocelot.services.repositories.pipeline import PipelineRepository
from ocelot.tests import TestCase

FAKE_UUID = 'fb624ae2-b219-49e2-ba01-cf81c72767f5'
FAKE_RECORD = {
    'name': 'foobar',
}


class TestPipelineRepository(TestCase):
    def test_fetch_pipeline_by_id(self):
        """Test that a record can be retrieved from the datastore."""
        self.set_config(
            'datastore.pipelines.{}'.format(FAKE_UUID),
            FAKE_RECORD,
        )

        expected_record = {}
        expected_record.update(FAKE_RECORD)
        expected_record.update({'id': FAKE_UUID})

        self.assertEquals(
            PipelineRepository.fetch_pipeline_by_id(FAKE_UUID),
            expected_record,
        )
