class PipelineScheduleTypes(object):
    cron = 'cron'
    interval = 'interval'


VALID_SCHEDULE_TYPES = (
    PipelineScheduleTypes.cron,
    PipelineScheduleTypes.interval,
)
