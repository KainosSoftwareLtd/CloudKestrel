import logging

from Config.ConfigHelper import ConfigHelper


logger = logging.getLogger('cloudkestrel')


# {
#     "Config": {
#         "Name": "IAM_USER_MFA_ENABLED",
#         "AddIfMissing": true,
#         "IgnoreUsers": ["SecurityReader"]
#     }
# }

class IamUserMfaEnabled(ConfigHelper):

    rule_name = 'IAM_USER_MFA_ENABLED'

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

