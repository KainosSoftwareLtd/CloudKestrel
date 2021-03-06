import logging

from Config.ConfigHelper import ConfigHelper

import codes
from Exceptions.ConfigRuleNotFoundException import ConfigRuleNotFoundException
from Exceptions.ConfigRuleNotAddedException import ConfigRuleNotAddedException
from Result import Result

logger = logging.getLogger('cloudkestrel')


# {
#     "Config": {
#         "Name": "IAM_ROOT_ACCESS_KEY_CHECK",
#         "AddIfMissing": true
#     }
# }

class IamRootAccessKeyCheck(ConfigHelper):

    rule_name = 'IAM_ROOT_ACCESS_KEY_CHECK'

    def __init__(self, session):
        self.session = session
        self.config = session.client('config')
        super().__init__(self.config)

    def add(self):
        logger.info('Adding compliance rule %s', self.rule_name)
        rule = {'ConfigRuleName': self.rule_name.lower(),
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': self.rule_name
                    }
                }
        return self.add_config_rule(rule)
