import redis

from ocelot import config


class Redis(object):
    @staticmethod
    def get(key):
        """Returns a value stored at a key.

        :param str key:
        :returns str: value stored at that key.
        """
        return Redis.get_client().get(key)

    @staticmethod
    def set(key, value):
        """Sets a key to a value.

        :param str key:
        :param str value:
        """
        return Redis.get_client().set(key, value)

    # TODO: this value should be cached off.
    # TODO: this should validate configuration
    @staticmethod
    def get_client():
        """Returns a configured StrictRedis client.

        :returns StrictRedis: Redis client.
        """
        return redis.StrictRedis(
            host=config.get('external.redis.host'),
            port=config.get('external.redis.port'),
            db=config.get('external.redis.db', 0),
        )
