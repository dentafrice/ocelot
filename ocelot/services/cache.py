from ocelot.services.gateways.redis import RedisGateway


class CacheService(object):
    @classmethod
    def fetch_value_for_key(cls, key):
        """Fetches value from the cache with the provided key.

        :param str key:
        :returns str: value
        """
        return RedisGateway.fetch_value_for_key(key)

    @classmethod
    def set_value_for_key(cls, key, value, ttl=None):
        """Sets a value at a specific key.

        :param str key:
        :param str value:
        :param int ttl: (optional) ttl in seconds
        """
        return RedisGateway.set_value_for_key(
            key,
            value,
            ttl=ttl,
        )
