

class FalseEvaluatingException(Exception):
    def __bool__(self):
        return False
    __nonzero__ = __bool__


class InvalidInputParameters(ValueError, FalseEvaluatingException):
    pass

class DeviceNotFound(RuntimeError, FalseEvaluatingException):
    pass