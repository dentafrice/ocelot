from ocelot.pipeline.channels.operations.dict_pattern_extractor_operation import (
    DictPatternExtractor,
)
from ocelot.pipeline.channels.operations.message_format_operation import MessageFormatOperation
from ocelot.pipeline.channels.operations.new_item_filter_operation import NewItemFilterOperation
from ocelot.pipeline.channels.operations.pluck_operation import PluckOperation
from ocelot.pipeline.channels.operations.xml_parse_operation import XMLParseOperation
from ocelot.pipeline.channels.operations.xml_rss_parse_operation import XMLRSSParseOperation

__all__ = [
    DictPatternExtractor,
    MessageFormatOperation,
    NewItemFilterOperation,
    PluckOperation,
    XMLParseOperation,
    XMLRSSParseOperation,
]
