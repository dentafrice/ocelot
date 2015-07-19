import hashlib
import pickle

from ocelot.lib import cache


class ChangeFilterOperation(object):
    def __init__(self, output, identifier, *args, **kwargs):
        self.output = output
        self.identifier = identifier

    def write(self, data):
        """Accepts and filters data from upstream.

        If the data has changed since last time, it will be written
        to the provided output, otherwise it will stop here.

        :param data:
        """
        for item in data:
            if self._allow(item):
                self.output.write([item])

    def _allow(self, data):
        """Returns whether or not to allow this data to pass the filter.

        :param data:
        :returns bool: whether or not we should allow this to pass.
        """
        data_hash = self._hash_data(
            self._serialize_data(data),
        )

        if self._get_cached_hash() == data_hash:
            return False

        self._update_cached_hash(data_hash)

        return True

    def _get_cached_hash(self):
        """Gets the value stored at the computed cache key.

        :returns str: stored hash or None
        """
        return cache.get(self._get_cache_key())

    def _update_cached_hash(self, data_hash):
        """Updates the hash that is stored in the cache.

        :param str data_hash: hash to store
        """
        return cache.set(self._get_cache_key(), data_hash)

    def _get_cache_key(self):
        """Returns the cache key for this class.

        :returns str: cache key
        """
        return 'cache:{}:{}'.format(
            self.__class__.__name__,
            self.identifier,
        )

    def _serialize_data(self, data):
        """Serializes the data to a hashable form.

        :param str data:
        :returns str: serialized data
        """
        return pickle.dumps(data)

    def _hash_data(self, data):
        """Converts data into a hash.

        :param str data:
        :returns str: data hash
        """
        return hashlib.sha256(data).hexdigest()
