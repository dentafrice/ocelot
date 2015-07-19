from ocelot.pipeline.channels.operations.change_filter_operation import ChangeFilterOperation
from ocelot.pipeline.channels.operations.dict_pattern_extractor_operation import (
    DictPatternExtractor,
)
from ocelot.pipeline.channels.operations.message_format_operation import MessageFormatOperation
from ocelot.pipeline.channels.operations.pluck_operation import PluckOperation
from ocelot.pipeline.channels.operations.xml_parse_operation import XMLParseOperation
from ocelot.pipeline.channels.operations.xml_rss_parse_operation import XMLRSSParseOperation

__all__ = [
    ChangeFilterOperation,
    DictPatternExtractor,
    MessageFormatOperation,
    PluckOperation,
    XMLParseOperation,
    XMLRSSParseOperation,
]
