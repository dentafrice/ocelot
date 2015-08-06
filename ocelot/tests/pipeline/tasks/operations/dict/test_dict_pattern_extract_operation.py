from ocelot.pipeline.exceptions import InvalidConfigurationException
from ocelot.pipeline.tasks.operations.dict_operation import (
    DictPatternExtractOperation,
)
from ocelot.tests import DatabaseTestCase


class TestDictPatternExtractOperation(DatabaseTestCase):
    def setUp(self):
        self.install_fixture('fake_dict')

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
            extractor.process(self.fake_dict)['level']['deep']['image'],
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
            extractor.process(self.fake_dict)
