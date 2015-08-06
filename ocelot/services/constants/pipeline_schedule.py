class PipelineScheduleTypes(object):
    """Represents the types of PipelineSchedules.

    cron: cron like schedule
    interval: run every X seconds.
    """
    cron = 'cron'
    interval = 'interval'
    manual = 'manual'


VALID_SCHEDULE_TYPES = (
    PipelineScheduleTypes.cron,
    PipelineScheduleTypes.interval,
    PipelineScheduleTypes.manual,
)
