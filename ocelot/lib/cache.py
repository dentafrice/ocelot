from ocelot.lib.external.redis_lib import Redis


def get(key):
    """Returns a value stored at a key.

    :param str key:
    :returns str: value
    """
    return Redis.get(key)


def set(key, value, ttl=None):
    """Sets a key to a value.

    :param str key:
    :param str value:
    """
    return Redis.set(key, value, ttl=ttl)
