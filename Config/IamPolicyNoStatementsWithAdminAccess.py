import logging

from Config.ConfigHelper import ConfigHelper


logger = logging.getLogger('cloudkestrel')


# {
#     "Config": {
#         "Name": "IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS",
#         "AddIfMissing": true
#     }
# }

class IamPolicyNoStatementsWithAdminAccess(ConfigHelper):

    rule_name = 'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS'

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

