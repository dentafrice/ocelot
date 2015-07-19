import hashlib
import pickle

from ocelot.lib import cache


class ChangeFilterOperation(object):
    def __init__(self, output, identifier, *args, **kwargs):
        self.output = output
        self.identifier = identifier

    def write(self, data):
        for item in data:
            if self._allow(item):
                self.output.write([item])

    def _allow(self, data):
        data_hash = self._hash_data(
            self._serialize_data(data),
        )

        if self._get_cache() == data_hash:
            return False

        self._update_cache(data_hash)

        return True

    def _get_cache(self):
        return cache.get(self._get_cache_key())

    def _update_cache(self, data_hash):
        return cache.set(self._get_cache_key(), data_hash)

    def _get_cache_key(self):
        return 'cache:{}:{}'.format(
            self.__class__.__name__,
            self.identifier,
        )

    def _serialize_data(self, data):
        return pickle.dumps(data)

    def _hash_data(self, data):
        return hashlib.sha256(data).hexdigest()
