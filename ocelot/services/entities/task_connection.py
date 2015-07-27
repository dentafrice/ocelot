import uuid

from schematics.types import UUIDType

from ocelot.services.entities.base_entity import BaseEntity


class TaskConnectionEntity(BaseEntity):
    id = UUIDType(
        default=lambda: uuid.uuid4(),
        required=True,
    )

    from_task_id = UUIDType(required=True)
    pipeline_id = UUIDType(required=True)
    to_task_id = UUIDType(required=True)
