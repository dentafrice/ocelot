from ocelot.pipeline.tasks.operations.dict_operation import (
    DictMapperOperation,
    DictPatternExtractOperation,
)
from ocelot.pipeline.tasks.operations.message_format_operation import MessageFormatOperation
from ocelot.pipeline.tasks.operations.new_item_filter_operation import NewItemFilterOperation
from ocelot.pipeline.tasks.operations.xml_parse_operation import XMLParseOperation
from ocelot.pipeline.tasks.operations.xml_rss_parse_operation import XMLRSSParseOperation

__all__ = [
    DictMapperOperation,
    DictPatternExtractOperation,
    MessageFormatOperation,
    NewItemFilterOperation,
    XMLParseOperation,
    XMLRSSParseOperation,
]
