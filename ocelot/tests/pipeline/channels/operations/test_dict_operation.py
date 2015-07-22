from ocelot.pipeline.channels.operations import (
    DictMapperOperation,
    DictPatternExtractOperation,
)
from ocelot.pipeline.exceptions import InvalidConfigurationException
from ocelot.tests import TestCase

FAKE_ITEM = {
    'level': {
        'array': [
            {
                'name': 'item1',
                'level': {
                    'value': 'sup',
                }
            },

            {
                'name': 'item2',
                'level': {
                    'value': 'sup',
                }
            },
        ],

        'deep': {
            'value': 'hey',
            'image': 'this is <img src="http://some.url/image.png"> cool',
        },
    }
}


class TestDictMapperOperation(TestCase):
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
            mapper.process(FAKE_ITEM),
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
            mapper.process(FAKE_ITEM),
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
            mapper.process(FAKE_ITEM),
            {
                'field1': FAKE_ITEM['level']['deep'],
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
            mapper.process(FAKE_ITEM),
            {
                'field1': 'sup',
            },
        )


class TestDictPatternExtractOperation(TestCase):
    def test_patterns_can_be_extracted(self):
        """Test that you can run a pattern on a path."""
        extractor = DictPatternExtractOperation(
            config={
                'paths': [
                    '$.level.deep.image'
                ],

                'pattern': 'src="(.*?)"',
            }
        )

        self.assertEquals(
            extractor.process(FAKE_ITEM)['level']['deep']['image'],
            'http://some.url/image.png',
        )

    def test_path_not_string(self):
        """Test that if a path doesn't match a string
        that an exception is raised."""
        extractor = DictPatternExtractOperation(
            config={
                'paths': [
                    '$.level.deep'
                ],

                'pattern': 'src="(.*?)"',
            }
        )

        with self.assertRaises(InvalidConfigurationException):
            extractor.process(FAKE_ITEM)
