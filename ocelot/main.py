from ocelot.pipeline.channels.inputs import URLInput
from ocelot.pipeline.channels.operations import DictMapperOperation
from ocelot.pipeline.channels.operations import DictPatternExtractOperation
from ocelot.pipeline.channels.operations import MessageFormatOperation
from ocelot.pipeline.channels.operations import NewItemFilterOperation
from ocelot.pipeline.channels.operations import XMLParseOperation
from ocelot.pipeline.channels.operations import XMLRSSParseOperation
from ocelot.pipeline.channels.outputs import LogOutput

from ocelot.pipeline.plumbing.pipeline import Pipeline


if __name__ == '__main__':
    pipeline = Pipeline(name='XKCD Check')

    # URL Input
    url = pipeline.add_channel(
        URLInput(url='http://xkcd.com/rss.xml'),
    )

    # XML Parser
    xml = pipeline.add_channel(
        XMLParseOperation()
    )

    # RSS Parser
    rss = pipeline.add_channel(
        XMLRSSParseOperation()
    )

    # New Item Filter
    new_item_filter = pipeline.add_channel(
        NewItemFilterOperation(
            identifier='xkcd-items',
        )
    )

    # Dict Extractor
    extractor = pipeline.add_channel(
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

    updater = pipeline.add_channel(
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
    message = pipeline.add_channel(
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
    log = pipeline.add_channel(
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
