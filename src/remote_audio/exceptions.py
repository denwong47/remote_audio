import traceback
from typing import Any


class FalseEvaluatingException(Exception):
    def __bool__(self):
        return False
    __nonzero__ = __bool__

    # This allows
    # with exception_causing_function() as cm:
    #    (cm is actually a FalseEvaluatingException instance)
    # 
    # This obviously will cause all sorts of Exception, the root cause being FalseEvaluatingException not being what the context block expected.
    # So we just throw the FalseEvaluatingException exception instead.
    def __enter__(self):
        return self
    
    def __exit__(
        self,
        exception_type:type,
        exception_message:str,
        exception_traceback:traceback):

        if (exception_type is not None):
            raise self
        return True

class WavFormatError(RuntimeError, FalseEvaluatingException):
    pass

class StreamIOError(OSError, FalseEvaluatingException):
    pass

class FileIOError(OSError, FalseEvaluatingException):
    pass

class HTTPIOError(RuntimeError, FalseEvaluatingException):
    pass

class InvalidInputParameters(ValueError, FalseEvaluatingException):
    pass

class DeviceNotFound(RuntimeError, FalseEvaluatingException):
    pass

