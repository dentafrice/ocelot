from ocelot.pipeline.operations.change_filter_operation import ChangeFilterOperation
from ocelot.pipeline.operations.dict_pattern_extractor_operation import DictPatternExtractor
from ocelot.pipeline.operations.message_format_operation import MessageFormatOperation
from ocelot.pipeline.operations.pluck_operation import PluckOperation
from ocelot.pipeline.operations.xml_parse_operation import XMLParseOperation
from ocelot.pipeline.operations.xml_rss_parse_operation import XMLRSSParseOperation

__all__ = [
    ChangeFilterOperation,
    DictPatternExtractor,
    MessageFormatOperation,
    PluckOperation,
    XMLParseOperation,
    XMLRSSParseOperation,
]
