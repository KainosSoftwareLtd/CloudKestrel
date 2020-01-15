from .BaseException import BaseException
from codes import POLICY_FOUND
from codes import POLICY_FOUND_FAIL


class PolicyNotFoundException(BaseException):
    """An Exception thrown when a policy isn't found."""

    def __init__(self, policy_name):
        desc = POLICY_FOUND_FAIL.format(policy_name)
        super().__init__(POLICY_FOUND, desc)
