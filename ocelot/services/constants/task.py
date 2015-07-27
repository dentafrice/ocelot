from ocelot.pipeline.tasks.inputs import URLInput
from ocelot.pipeline.tasks.operations import DictCreateOperation
from ocelot.pipeline.tasks.operations import DictMapperOperation
from ocelot.pipeline.tasks.operations import DictPatternExtractOperation
from ocelot.pipeline.tasks.operations import MessageFormatOperation
from ocelot.pipeline.tasks.operations import NewItemFilterOperation
from ocelot.pipeline.tasks.operations import XMLParseOperation
from ocelot.pipeline.tasks.operations import XMLRSSParseOperation
from ocelot.pipeline.tasks.outputs import LogOutput
from ocelot.pipeline.tasks.outputs import EmailOutput


TASK_MAP = {
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
