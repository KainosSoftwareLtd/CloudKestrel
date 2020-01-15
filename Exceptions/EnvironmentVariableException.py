from .BaseException import BaseException
from codes import ENVIRONMENT_VARIABLE
from codes import ENVIRONMENT_VARIABLE_FAIL


class EnvironmentVariableException(BaseException):
    """An Exception thrown when there are missing environment variables."""

    def __init__(self, variable_name, target):
        desc = ENVIRONMENT_VARIABLE_FAIL.format(variable_name, target)
        super().__init__(ENVIRONMENT_VARIABLE, desc)
