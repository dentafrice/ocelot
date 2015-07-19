import uuid

from ocelot.pipeline.channels.inputs import URLInput
from ocelot.pipeline.channels.operations import ChangeFilterOperation
from ocelot.pipeline.channels.operations import DictPatternExtractor
from ocelot.pipeline.channels.operations import MessageFormatOperation
from ocelot.pipeline.channels.operations import PluckOperation
from ocelot.pipeline.channels.operations import XMLParseOperation
from ocelot.pipeline.channels.operations import XMLRSSParseOperation
from ocelot.pipeline.channels.outputs import LogOutput

if __name__ == '__main__':
    url = URLInput(
        url='http://xkcd.com/rss.xml',
    )

    change = ChangeFilterOperation(
        # identifier='xkcd-rss',
        identifier=str(uuid.uuid4()),
    )

    xml = XMLParseOperation()
    rss = XMLRSSParseOperation()
    pluck = PluckOperation(
        fields=['title', 'description'],
    )
    pattern = DictPatternExtractor(
        config={
            'description': 'src="(.*?)"',
        }
    )
    message_format = MessageFormatOperation(
        message="""
        XKCD Lineup:
        ----
        {% for item in data %}
        {{item.title}}
        {{item.description}}
        {% endfor %}
        """,
    )

    log = LogOutput(log_name='xkcd')

    log.process(
        message_format.process(
            pattern.process(
                pluck.process(
                    rss.process(
                        xml.process(
                            change.process(
                                url.process(None)
                            )
                        )
                    )
                )
            )
        )
    )
