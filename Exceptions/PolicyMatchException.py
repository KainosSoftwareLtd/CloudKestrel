from .BaseException import BaseException
from codes import POLICY_MATCH
from codes import POLICY_MATCH_FAIL


class PolicyMatchException(BaseException):
    """An Exception thrown when policies don't match."""

    def __init__(self, policy_name, fails):
        desc = POLICY_MATCH_FAIL.format(policy_name, fails)
        super().__init__(POLICY_MATCH, desc)
