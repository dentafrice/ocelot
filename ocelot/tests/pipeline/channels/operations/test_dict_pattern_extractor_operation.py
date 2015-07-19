import mock

from ocelot.pipeline.channels.operations import DictPatternExtractor
from ocelot.tests import TestCase

FAKE_DICTS = [
    {'title': 't1', 'description': 'sfs<img src="foobar"> adfklaj'},
    {'title': 't2', 'description': 'adf<img src="foobar2">af daklsjfalkj'},
]


class FakeOutput(object):
    def write(self, *args, **kwargs):
        pass


class TestDictPatternExtractor(TestCase):
    @mock.patch.object(FakeOutput, 'write')
    def test_write_extracted_fields(self, mock_output_write):
        """Test that write will write the new dict to the output."""
        extractor = DictPatternExtractor(
            output=FakeOutput(),
            config={
                'description': 'src="(.*?)"',
            }
        )

        extractor.write([FAKE_DICTS])

        mock_output_write.assert_called_once_with([[
            {'title': 't1', 'description': 'foobar'},
            {'title': 't2', 'description': 'foobar2'},
        ]])

    @mock.patch.object(FakeOutput, 'write')
    def test_write_single_dict(self, mock_output_write):
        """Test that write works with a single dict instead of a list."""
        extractor = DictPatternExtractor(
            output=FakeOutput(),
            config={
                'description': 'src="(.*?)"',
            }
        )

        extractor.write([FAKE_DICTS[0]])

        mock_output_write.assert_called_once_with([
            {'title': 't1', 'description': 'foobar'},
        ])
