from ocelot.pipeline.tasks.operations.dict_operation import (
    DictMapperOperation,
)
from ocelot.tests import DatabaseTestCase


class TestDictMapperOperation(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('fake_dict')

    def test_values_are_extracted(self):
        """Test that a value can be extracted."""
        mapper = DictMapperOperation(
            config={
                'field1': {
                    'type': 'extract',
                    'config': {
                        'path': '$.level.deep.value',
                    }
                }
            }
        )

        self.assertEquals(
            mapper.process(self.fake_dict),
            {
                'field1': 'hey',
            },
        )

    def test_non_existant_path(self):
        """Test that a path that doesn't exist
        gets turned into None."""
        mapper = DictMapperOperation(
            config={
                'field1': {
                    'type': 'extract',
                    'config': {
                        'path': '$.to.mars.and.back',
                    }
                }
            }
        )

        self.assertEquals(
            mapper.process(self.fake_dict),
            {
                'field1': None,
            },
        )

    def test_matching_whole_dicts(self):
        """Test that you can extract an entire dict."""
        mapper = DictMapperOperation(
            config={
                'field1': {
                    'type': 'extract',
                    'config': {
                        'path': '$.level.deep',
                    }
                }
            }
        )

        self.assertEquals(
            mapper.process(self.fake_dict),
            {
                'field1': self.fake_dict['level']['deep'],
            },
        )

    def test_access_array(self):
        """Test that you can extract values from an array."""
        mapper = DictMapperOperation(
            config={
                'field1': {
                    'type': 'extract',
                    'config': {
                        'path': '$.level.array.[0].level.value',
                    }
                }
            }
        )

        self.assertEquals(
            mapper.process(self.fake_dict),
            {
                'field1': 'sup',
            },
        )

    def test_insert(self):
        """Test that a value can be inserted."""
        mapper = DictMapperOperation(
            config={
                'field1': {
                    'type': 'insert',
                    'config': {
                        'value': 'foo bar baz',
                    }
                }
            }
        )

        self.assertEquals(
            mapper.process(self.fake_dict),
            {
                'field1': 'foo bar baz',
            }
        )
