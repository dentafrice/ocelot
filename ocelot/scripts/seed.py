import json

from sqlalchemy.exc import IntegrityError

from ocelot.services import datastores
from ocelot.services.datastores import (
    PipelineStore,
    PipelineScheduleStore,
    Session,
    TaskConnectionStore,
    TaskStore,
)
from ocelot.services.pipeline_schedule import PipelineScheduleService


def create_datastore(datastore):
    try:
        Session.add(datastore)
        Session.commit()

        return datastore
    except IntegrityError:
        Session.rollback()

        return datastore


if __name__ == '__main__':
    datastores.create_tables()
    datastores.initialize()

    pipeline = create_datastore(PipelineStore(
        id='96feda22-f80d-4cee-ad51-4e18de0b655a',
        name='XKCD Check',
    ))

    create_datastore(PipelineScheduleStore(
        pipeline_id=pipeline.id,

        # Interval Schedule
        schedule=str(21600),  # 6hrs in seconds
        type='interval',

        # Cron schedule
        #  schedule='* * * * *',
        #  type='cron',
    ))
    PipelineScheduleService.update_next_run_at_for_pipeline(pipeline.id)

    url = create_datastore(TaskStore(
        id='cb332d4f-3f51-4a89-b68b-edf1a0b882f0',
        type='URLInput',
        config=json.dumps({
            'url': 'http://xkcd.com/rss.xml',
        }),
    ))

    xml = create_datastore(TaskStore(
        id='4cde9299-706c-4375-a82d-640980bc6bf4',
        type='XMLParseOperation',
    ))

    rss = create_datastore(TaskStore(
        id='293e636f-75ec-4326-bfea-475822e429b6',
        type='XMLRSSParseOperation',
    ))

    new_filter = create_datastore(TaskStore(
        id='c3b2b54c-4cda-43ee-b4f6-b63436806d64',
        type='NewItemFilterOperation',
        config=json.dumps({
            'identifier': 'xkcd-items',
        }),
    ))

    item_mapper = create_datastore(TaskStore(
        id='af39bfda-8187-4b73-9759-7e325811b952',
        type='DictMapperOperation',
        config=json.dumps({
            'config': {
                'title': {
                    'type': 'extract',
                    'config': {
                        'path': '$.title',
                    },
                },

                'description': {
                    'type': 'extract',
                    'config': {
                        'path': '$.description',
                    },
                },
            },
        }),
    ))

    pattern_extract = create_datastore(TaskStore(
        id='c9e82e66-3d07-42ec-bcdc-d20050f7b592',
        type='DictPatternExtractOperation',
        config=json.dumps({
            'config': {
                'paths': [
                    '$.description',
                ],

                'pattern': 'src="(.*?)"',
            },
        }),
    ))

    message_format = create_datastore(TaskStore(
        id='18887ac8-a2a8-47b0-a9d6-91528b8cf87d',
        type='MessageFormatOperation',
        config=json.dumps({
            'message': """XKCD Lineup:
---
{% for item in data %}
{{item.title}}
{{item.description}}
{% endfor %}
""",
        }),
    ))

    dict_create = create_datastore(TaskStore(
        id='15b3a330-2bcc-4cbb-bb53-d894244f0f27',
        type='DictCreateOperation',
        config=json.dumps({
            'config': {
                'key': 'plain_message',
            },
        }),
    ))

    email_mapper = create_datastore(TaskStore(
        id='cad413a2-869c-4c82-84e4-df459a31acf9',
        type='DictMapperOperation',
        config=json.dumps({
            'config': {
                'plain_message': {
                    'type': 'extract',
                    'config': {
                        'path': '$.plain_message',
                    },
                },

                'from_email': {
                    'type': 'insert',
                    'config': {
                        'value': 'ocelot@caleb.io',
                    },
                },

                'subject': {
                    'type': 'insert',
                    'config': {
                        'value': 'New XKCD Items',
                    },
                },

                'to_email': {
                    'type': 'insert',
                    'config': {
                        'value': 'me@caleb.io',
                    },
                },
            },
        }),
    ))

    log_output = create_datastore(TaskStore(
        id='b40786e1-dbb2-43ab-a074-a0fd74211d97',
        type='LogOutput',
        config=json.dumps({
            'log_name': 'xkcd',
        }),
    ))

    email_output = create_datastore(TaskStore(
        id='e74fbf87-f15a-4286-a8ee-e80ddbe756a5',
        type='EmailOutput',
    ))

    # Connections

    create_datastore(TaskConnectionStore(
        id='c76107e3-0d11-4867-a56a-18cdd0d379c8',
        from_task_id=url.id,
        to_task_id=xml.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='998ce7e0-d09b-4440-bfec-864e0e7f95f3',
        from_task_id=xml.id,
        to_task_id=rss.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='50818c41-9d5e-4300-8c80-73dc40973c17',
        from_task_id=rss.id,
        to_task_id=new_filter.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='aaff7cc3-136e-449e-9fed-54fa000c1e72',
        from_task_id=new_filter.id,
        to_task_id=item_mapper.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='a2fcaf7f-c633-4bb9-a674-64e018221f22',
        from_task_id=item_mapper.id,
        to_task_id=pattern_extract.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='71bf5cbe-975a-45f0-a90b-f586dc01232c',
        from_task_id=pattern_extract.id,
        to_task_id=message_format.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='f09edb7a-d255-4e0d-9b28-62809d63c665',
        from_task_id=message_format.id,
        to_task_id=dict_create.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='799da080-bf80-4573-a729-997ba0900cbc',
        from_task_id=dict_create.id,
        to_task_id=email_mapper.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='49ca8ca8-5355-4ee1-bb4d-ad23ae3d1f68',
        from_task_id=email_mapper.id,
        to_task_id=log_output.id,
        pipeline_id=pipeline.id,
    ))

    create_datastore(TaskConnectionStore(
        id='1f65df09-5cb8-414d-87bd-606f256c3cec',
        from_task_id=email_mapper.id,
        to_task_id=email_output.id,
        pipeline_id=pipeline.id,
    ))
