import uuid

from ocelot.pipeline.channels.inputs import URLInput
from ocelot.pipeline.channels.operations import ChangeFilterOperation
from ocelot.pipeline.channels.operations import DictPatternExtractor
from ocelot.pipeline.channels.operations import MessageFormatOperation
from ocelot.pipeline.channels.operations import PluckOperation
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

    # Change Filter
    change = pipeline.add_channel(
        # identifier='xkcd-rss',
        ChangeFilterOperation(identifier=str(uuid.uuid4()))
    )

    # XML Parser
    xml = pipeline.add_channel(
        XMLParseOperation()
    )

    # RSS Parser
    rss = pipeline.add_channel(
        XMLRSSParseOperation()
    )

    # Field Plucker
    plucker = pipeline.add_channel(
        PluckOperation(fields=['title', 'description'])
    )

    # Pattern Extractor
    pattern = pipeline.add_channel(
        DictPatternExtractor(config={'description': 'src="(.*?)"'})
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
    url.connect_fitting(change)
    change.connect_fitting(xml)
    xml.connect_fitting(rss)
    rss.connect_fitting(plucker)
    plucker.connect_fitting(pattern)
    pattern.connect_fitting(message)
    message.connect_fitting(log)

    # Run pipeline
    pipeline.run()
