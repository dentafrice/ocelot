from ocelot.pipeline.inputs import URLInput
from ocelot.pipeline.outputs import LogOutput

if __name__ == '__main__':
    l = LogOutput('xkcd')

    u = URLInput(
        output=l,
        url='http://xkcd.com/rss.xml',
    )

    u.run()
