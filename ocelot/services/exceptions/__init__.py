class BaseOcelotException(Exception):
    """Base Ocelot service exception."""


class ResourceNotFoundException(BaseOcelotException):
    """Raised when a resource could not be found."""
