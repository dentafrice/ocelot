import requests


class URLInput(object):
    def __init__(self, output, url, *args, **kwargs):
        self.output = output
        self.url = url

    def run(self):
        self.output.write(
            self._make_request()
        )

    def _make_request(self):
        return requests.get(self.url).content
