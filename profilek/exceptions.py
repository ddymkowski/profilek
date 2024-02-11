class BaseProfilerException(Exception):
    """Base exception for data profiler"""


class UnsupportedFileTypeException(BaseProfilerException):
    """Handles unsupported input types"""


class InputFileNotFoundException(BaseProfilerException):
    """Handles unexisting files"""


class InvalidSchemaException(BaseProfilerException):
    """Handles schema issues on read"""


class UserPluginMappingException(BaseProfilerException):
    """Handles issues with user to plugin mapping"""