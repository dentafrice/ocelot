from ocelot.lib.external.redis_lib import Redis


def get(key):
    return Redis.get(key)


def set(key, value):
    return Redis.set(key, value)
