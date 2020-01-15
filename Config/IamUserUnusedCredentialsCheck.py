import logging

from Config.ConfigHelper import ConfigHelper


logger = logging.getLogger('cloudkestrel')


# {
#     "Config": {
#         "Name": "IAM_USER_UNUSED_CREDENTIALS_CHECK",
#         "AddIfMissing": true
#     }
# }

class IamUserUnusedCredentialsCheck(ConfigHelper):

    rule_name = 'IAM_USER_UNUSED_CREDENTIALS_CHECK'

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
                },
                'InputParameters': '{\"maxCredentialUsageAge\":\"4\"}'
                }
        return self.add_config_rule(rule)

