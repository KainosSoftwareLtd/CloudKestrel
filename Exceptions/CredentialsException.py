from .BaseException import BaseException
from codes import CREDENTIALS
from codes import CREDENTIALS_FAIL


class CredentialsException(BaseException):
    """An Exception thrown when there are missing environment variables."""

    def __init__(self, error):
        desc = CREDENTIALS_FAIL.format(error)
        super().__init__(CREDENTIALS, desc)
