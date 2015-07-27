import uuid

from schematics.types import BaseType, StringType, UUIDType
from schematics.types.compound import DictType

from ocelot.services.constants.task import VALID_TASK_TYPES
from ocelot.services.entities.base_entity import BaseEntity


class TaskEntity(BaseEntity):
    config = DictType(
        BaseType,
        default=lambda: {},
        required=True,
    )

    id = UUIDType(
        default=lambda: uuid.uuid4(),
        required=True,
    )

    type = StringType(
        choices=VALID_TASK_TYPES,
        required=True,
    )
