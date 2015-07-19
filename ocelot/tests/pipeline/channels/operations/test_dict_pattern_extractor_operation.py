from ocelot.pipeline.channels.operations import DictPatternExtractor
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'title': 't1', 'description': 'sfs<img src="foobar"> adfklaj'},
    {'title': 't2', 'description': 'adf<img src="foobar2">af daklsjfalkj'},
]


class TestDictPatternExtractor(TestCase):
    def test_process_extracted_fields(self):
        """Test that process will process the new dict to the output."""
        extractor = DictPatternExtractor(
            config={
                'description': 'src="(.*?)"',
            }
        )

        self.assertEquals(
            extractor.process(FAKE_DICTS),
            [
                {'title': 't1', 'description': 'foobar'},
                {'title': 't2', 'description': 'foobar2'},
            ],
        )

    def test_process_single_dict(self):
        """Test that process works with a single dict instead of a list."""
        extractor = DictPatternExtractor(
            config={
                'description': 'src="(.*?)"',
            }
        )

        self.assertEquals(
            extractor.process(FAKE_DICTS[0]),
            {'title': 't1', 'description': 'foobar'},
        )
