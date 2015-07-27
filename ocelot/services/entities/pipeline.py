import uuid

from schematics.types import StringType, UUIDType

from ocelot.services.entities.base_entity import BaseEntity


class PipelineEntity(BaseEntity):
    id = UUIDType(
        default=lambda: uuid.uuid4(),
        required=True,
    )

    name = StringType(required=True)
