import requests


class URLInput(object):
    def __init__(self, output, url, *args, **kwargs):
        self.output = output
        self.url = url

    def run(self):
        """Makes the HTTP request to the provided URL and writes it to the
        output."""
        self.output.write(
            [self._make_request()],
        )

    def _make_request(self):
        """Makes an HTTP request to the provided URL and returns the raw content.

        :returns str: content
        """
        return requests.get(self.url).content
