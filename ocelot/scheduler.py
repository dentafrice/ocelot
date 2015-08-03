import time

from ocelot.lib import logging
from ocelot.services import datastores
from ocelot.services.pipeline import PipelineService
from ocelot.services.pipeline_schedule import PipelineScheduleService

log = logging.getLogger('ocelot.scheduler')

SLEEP_SECONDS = 10

if __name__ == '__main__':
    datastores.create_tables()
    datastores.initialize()

    log.info('Starting scheduler')

    try:
        while True:
            log.info('Fetching pipelines to run')
            pipeline_schedules = PipelineScheduleService.fetch_schedules_to_run()

            log.info('Found {} pipelines to run'.format(len(pipeline_schedules)))

            for schedule in PipelineScheduleService.fetch_schedules_to_run():
                PipelineService.run_pipeline_by_id(schedule.pipeline_id)

            log.info('Sleeping {} seconds'.format(SLEEP_SECONDS))
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        pass

    log.info('Shutting down scheduler')
