class BaseOcelotException(Exception):
    pass


class ResourceNotFoundException(BaseOcelotException):
    """Raised when a resource could not be found."""
