from ocelot.pipeline.tasks.inputs.raw_input import RawInput
from ocelot.pipeline.tasks.inputs.url_input import URLInput
from ocelot.pipeline.tasks.operations.dict.dict_create_operation import DictCreateOperation
from ocelot.pipeline.tasks.operations.dict.dict_mapper_operation import DictMapperOperation
from ocelot.pipeline.tasks.operations.dict.dict_pattern_extract_operation import (
    DictPatternExtractOperation,
)
from ocelot.pipeline.tasks.operations.message_format_operation import MessageFormatOperation
from ocelot.pipeline.tasks.operations.new_item_filter_operation import NewItemFilterOperation
from ocelot.pipeline.tasks.operations.xml_parse_operation import XMLParseOperation
from ocelot.pipeline.tasks.operations.xml_rss_parse_operation import XMLRSSParseOperation
from ocelot.pipeline.tasks.outputs.log_output import LogOutput
from ocelot.pipeline.tasks.outputs.email_output import EmailOutput


TASK_MAP = {
    'RawInput': RawInput,
    'URLInput': URLInput,
    'DictCreateOperation': DictCreateOperation,
    'DictMapperOperation': DictMapperOperation,
    'DictPatternExtractOperation': DictPatternExtractOperation,
    'MessageFormatOperation': MessageFormatOperation,
    'NewItemFilterOperation': NewItemFilterOperation,
    'XMLParseOperation': XMLParseOperation,
    'XMLRSSParseOperation': XMLRSSParseOperation,
    'EmailOutput': EmailOutput,
    'LogOutput': LogOutput,
}

VALID_TASK_TYPES = TASK_MAP.keys()
