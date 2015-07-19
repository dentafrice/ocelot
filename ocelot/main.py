from ocelot.pipeline.channels.inputs import URLInput
from ocelot.pipeline.channels.operations import ChangeFilterOperation
from ocelot.pipeline.channels.operations import DictPatternExtractor
from ocelot.pipeline.channels.operations import MessageFormatOperation
from ocelot.pipeline.channels.operations import PluckOperation
from ocelot.pipeline.channels.operations import XMLParseOperation
from ocelot.pipeline.channels.operations import XMLRSSParseOperation
from ocelot.pipeline.channels.outputs import LogOutput

if __name__ == '__main__':
    LogOutput(
        log_name='xkcd',
    )

    URLInput(
        output=ChangeFilterOperation(
            output=XMLParseOperation(
                output=XMLRSSParseOperation(
                    output=PluckOperation(
                        output=DictPatternExtractor(
                            output=MessageFormatOperation(
                                output=LogOutput(
                                    log_name='xkcd',
                                ),

                                message="""
XKCD Lineup:
----
{% for item in data %}
{{item.title}}
{{item.description}}
{% endfor %}
""",
                            ),

                            config={
                                'description': 'src="(.*?)"',
                            },
                        ),

                        fields=['title', 'description'],
                    ),
                ),
            ),

            identifier='xkcd-rss',
        ),

        url='http://xkcd.com/rss.xml',
    ).run()
