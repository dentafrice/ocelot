from __future__ import absolute_import

import redis

from ocelot import config


class RedisGateway(object):
    @classmethod
    def fetch_value_for_key(cls, key):
        """Fetches value from the cache with the provided key.

        :param str key:
        :returns str: value
        """
        return cls.get_client().get(key)

    @classmethod
    def set_value_for_key(cls, key, value, ttl=None):
        """Sets a value at a specific key.

        :param str key:
        :param str value:
        :param int ttl: (optional) ttl in seconds
        """
        print key, value, ttl
        if ttl is not None:
            return cls.get_client().setex(key, ttl, value)

        return cls.get_client().set(key, value)

    # TODO: this value should be cached off.
    # TODO: this should validate configuration
    @classmethod
    def get_client(cls):
        """Returns a configured StrictRedis client.

        :returns StrictRedis: Redis client.
        """
        return redis.StrictRedis(
            host=config.get('external.redis.host'),
            port=config.get('external.redis.port'),
            db=config.get('external.redis.db', 0),
        )
