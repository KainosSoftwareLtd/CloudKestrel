from .BaseException import BaseException
from codes import CONFIG_RULE_FOUND
from codes import CONFIG_RULE_FOUND_FAIL


class ConfigRuleNotFoundException(BaseException):
    """An Exception thrown when a config rule isn't found."""

    def __init__(self, config_rule_name):
        desc = CONFIG_RULE_FOUND_FAIL.format(config_rule_name)
        super().__init__(CONFIG_RULE_FOUND, desc)
