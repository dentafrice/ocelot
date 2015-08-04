import functools

from ocelot.services.datastores import NoResultFound
from ocelot.services.exceptions import ResourceNotFoundException


def handle_no_result_found(func):
    """Catches NoResultFound and raises a ResourceNotFoundException.

    :param func func:
    :returns func: wrapped function
    :raises ResourceNotFoundException: if resource is not found
    """
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            raise ResourceNotFoundException

    return wrapped_func
