


    

from re import L


class FalseEvaluatingException(Exception):
    def __bool__(self):
        return False
    __nonzero__ = __bool__

class FileIOError(OSError, FalseEvaluatingException):
    pass

class HTTPIOError(RuntimeError, FalseEvaluatingException):
    pass

class InvalidInputParameters(ValueError, FalseEvaluatingException):
    pass

class DeviceNotFound(RuntimeError, FalseEvaluatingException):
    pass