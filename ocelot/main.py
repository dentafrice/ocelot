from ocelot.pipeline.inputs import URLInput
from ocelot.pipeline.operations import DictPatternExtractor
from ocelot.pipeline.operations import MessageFormatOperation
from ocelot.pipeline.operations import PluckOperation
from ocelot.pipeline.operations import XMLParseOperation
from ocelot.pipeline.operations import XMLRSSParseOperation
from ocelot.pipeline.outputs import LogOutput

if __name__ == '__main__':
    URLInput(
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

        url='http://xkcd.com/rss.xml',
    ).run()
