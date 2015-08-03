from ocelot.services import datastores
from ocelot.services.pipeline import PipelineService
from ocelot.services.pipeline_schedule import PipelineScheduleService

if __name__ == '__main__':
    datastores.create_tables()
    datastores.initialize()

    pipeline_schedules = PipelineScheduleService.fetch_schedules_to_run()

    for schedule in PipelineScheduleService.fetch_schedules_to_run():
        PipelineService.run_pipeline_by_id(schedule.pipeline_id)
