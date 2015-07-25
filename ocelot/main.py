from ocelot.pipeline.tasks.inputs import URLInput
from ocelot.pipeline.tasks.operations import DictMapperOperation
from ocelot.pipeline.tasks.operations import DictPatternExtractOperation
from ocelot.pipeline.tasks.operations import MessageFormatOperation
from ocelot.pipeline.tasks.operations import NewItemFilterOperation
from ocelot.pipeline.tasks.operations import XMLParseOperation
from ocelot.pipeline.tasks.operations import XMLRSSParseOperation
from ocelot.pipeline.tasks.outputs import LogOutput

from ocelot.pipeline.plumbing.pipeline import Pipeline


if __name__ == '__main__':
    pipeline = Pipeline(name='XKCD Check')

    # URL Input
    url = pipeline.add_task(
        URLInput(url='http://xkcd.com/rss.xml'),
    )

    # XML Parser
    xml = pipeline.add_task(
        XMLParseOperation()
    )

    # RSS Parser
    rss = pipeline.add_task(
        XMLRSSParseOperation()
    )

    # New Item Filter
    new_item_filter = pipeline.add_task(
        NewItemFilterOperation(
            identifier='xkcd-items',
        )
    )

    # Dict Extractor
    extractor = pipeline.add_task(
        DictMapperOperation(
            config={
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
                    }
                },
            }
        )
    )

    updater = pipeline.add_task(
        DictPatternExtractOperation(
            config={
                'paths': [
                    '$.description',
                ],

                'pattern': 'src="(.*?)"',
            },
        )
    )

    # Message Formatter
    message = pipeline.add_task(
        MessageFormatOperation(
            message="""
            XKCD Lineup:
            ----
            {% for item in data %}
            {{item.title}}
            {{item.description}}
            {% endfor %}
            """
        )
    )

    # Log Output
    log = pipeline.add_task(
        LogOutput(log_name='xkcd')
    )

    # Connections
    url.connect_fitting(xml)
    xml.connect_fitting(rss)
    rss.connect_fitting(extractor)
    # rss.connect_fitting(new_item_filter)
    # new_item_filter.connect_fitting(extractor)
    extractor.connect_fitting(updater)
    updater.connect_fitting(message)
    message.connect_fitting(log)

    # Run pipeline
    pipeline.run()
