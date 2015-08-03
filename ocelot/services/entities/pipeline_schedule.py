from schematics.types import BooleanType, DateTimeType, StringType, UUIDType

from ocelot.services.constants.pipeline_schedule import VALID_SCHEDULE_TYPES
from ocelot.services.entities.base_entity import BaseEntity


class PipelineScheduleEntity(BaseEntity):
    pipeline_id = UUIDType(required=True)

    schedule = StringType(required=True)
    schedule_type = StringType(
        choices=VALID_SCHEDULE_TYPES,
        required=True,
    )

    next_run_at = DateTimeType(required=True)
    last_run_at = DateTimeType()

    locked = BooleanType(required=True, default=False)
