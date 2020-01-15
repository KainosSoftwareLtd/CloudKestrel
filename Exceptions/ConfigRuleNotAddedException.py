from .BaseException import BaseException
from codes import CONFIG_RULE_ADDED
from codes import CONFIG_RULE_ADDED_FAIL


class ConfigRuleNotAddedException(BaseException):
    """An Exception thrown when a config rule can't be added."""

    def __init__(self, config_rule_name):
        desc = CONFIG_RULE_ADDED_FAIL.format(config_rule_name)
        super().__init__(CONFIG_RULE_ADDED, desc)
