import hashlib
import pickle

from ocelot.pipeline.tasks.operations.base_operation import BaseOperation
from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.services.cache import CacheService


class NewItemFilterOperation(BaseOperation):
    def __init__(self, identifier, *args, **kwargs):
        self.identifier = identifier

        super(NewItemFilterOperation, self).__init__(*args, **kwargs)

    def process(self, data):
        """Checks to see if the provided data has changed since the filter was last run.

        If the data has changed:
            Unmodified data will be returned

        If the data has not changed:
            StopProcessingException will be raised.

        :param object data:
        :returns: data if filter passes
        :raises StopProcessingException: if the data has not changed.
        """
        new_items = [
            item for item in data
            if self._allow(item)
        ]

        if new_items:
            return new_items

        raise StopProcessingException('No new items found')

    def _allow(self, data):
        """Returns whether or not to allow this data to pass the filter.

        :param object data:
        :returns bool: whether or not we should allow this to pass.
        """
        data_hash = self._hash_data(
            self._serialize_data(data),
        )

        if self._has_seen_hash(data_hash):
            return False

        self._mark_hash_seen(data_hash)

        return True

    def _has_seen_hash(self, data_hash):
        """Gets the value stored at the computed cache key.

        :param str data_hash:
        :returns bool: whether or not the hash is in the cache.
        """
        return bool(
            CacheService.fetch_value_for_key(
                self._get_cache_key(data_hash)
            )
        )

    def _mark_hash_seen(self, data_hash):
        """Adds the data hash to the cache.

        :param str data_hash: hash to store
        """
        CacheService.set_value_for_key(
            self._get_cache_key(data_hash),
            data_hash,
        )

    def _get_cache_key(self, data_hash):
        """Returns the cache key for this class.

        :param str data_hash:
        :returns str: cache key
        """
        return 'cache:{}:{}:{}'.format(
            self.__class__.__name__,
            self.identifier,
            data_hash,
        )

    def _serialize_data(self, data):
        """Serializes the data to a hashable form.

        Uses pickle to serialize data.

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
