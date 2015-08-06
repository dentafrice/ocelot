from schematics.exceptions import ValidationError
from schematics.types import BooleanType, DateTimeType, StringType, UUIDType

from ocelot.services.constants.pipeline_schedule import (
    PipelineScheduleTypes,
    VALID_SCHEDULE_TYPES,
)
from ocelot.services.entities.base_entity import BaseEntity


class PipelineScheduleEntity(BaseEntity):
    pipeline_id = UUIDType(required=True)

    schedule = StringType()
    type = StringType(
        choices=VALID_SCHEDULE_TYPES,
        required=True,
    )

    next_run_at = DateTimeType()
    last_run_at = DateTimeType()

    locked = BooleanType(required=True, default=False)

    def validate_next_run_at(self, data, value):
        """Validate that next_run_at is provided for all schedule types except manual."""
        if not value and data['type'] != PipelineScheduleTypes.manual:
            raise ValidationError(
                'A next_run_at is required for this type: {}'.format(data['type'])
            )

    def validate_schedule(self, data, value):
        """Validate that a schedule is provided for all schedule types except manual."""
        if not value and data['type'] != PipelineScheduleTypes.manual:
            raise ValidationError('A schedule is required for this type: {}'.format(data['type']))
