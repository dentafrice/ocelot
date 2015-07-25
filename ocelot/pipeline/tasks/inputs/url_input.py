import requests

from ocelot.pipeline.tasks.inputs.base_input import BaseInput


class URLInput(BaseInput):
    def __init__(self, url, *args, **kwargs):
        self.url = url

        super(URLInput, self).__init__(*args, **kwargs)

    def process(self, data):
        """Makes the HTTP request to the provided URL and writes it to the
        output.

        :param data:
        :returns str: HTTP response
        """
        return self._make_request()

    def _make_request(self):
        """Makes an HTTP request to the provided URL and returns the raw content.

        :returns str: content
        """
        return requests.get(self.url).content
