"""wagoplc.exceptions
All library exceptions.
"""

class WAGOPlcError(Exception):
    """Base class for WAGO PLC related errors."""
    pass

class NotDefinedError(WAGOPlcError):
    """Raised when a variable in a task function is not defined in IO mapping."""
    pass

class WatchdogTimeoutError(WAGOPlcError):
    """Throw when task cycle exceeds maximum allowed time."""
    pass

class NonExistingIOError(WAGOPlcError):
    """Throw when a not existing IO is trying to be reached."""
    pass

class InvalidConfigError(WAGOPlcError):
    """Throw when an invalid configuration was given."""
    pass