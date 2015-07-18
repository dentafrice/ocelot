from ocelot.pipeline.inputs import URLInput
from ocelot.pipeline.operations import XMLParseOperation
from ocelot.pipeline.operations import XMLRSSParseOperation
from ocelot.pipeline.outputs import LogOutput

if __name__ == '__main__':
    URLInput(
        output=XMLParseOperation(
            output=XMLRSSParseOperation(
                output=LogOutput(
                    log_name='xkcd',
                ),
            ),
        ),

        url='http://xkcd.com/rss.xml',
    ).run()
