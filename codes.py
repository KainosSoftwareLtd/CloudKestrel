# Codes and descriptions for all results and exceptions
ENVIRONMENT_VARIABLE = 'ENVIRONMENT_VARIABLE'
ENVIRONMENT_VARIABLE_FAIL = 'Environment variable {} missing for target {}'

CREDENTIALS = 'CREDENTIALS'
CREDENTIALS_FAIL = 'Failed to connect with credentials, error: {}'

POLICY_FOUND = 'POLICY_FOUND'
POLICY_FOUND_SUCCESS = 'Policy {} found'
POLICY_FOUND_FAIL = 'Policy {} not found'

POLICY_MATCH = 'POLICY_MATCH'
POLICY_MATCH_SUCCESS = 'Policy match for policy {}'
POLICY_MATCH_FAIL = 'Policy match fail for policy {} with errors {}'

USER_HAS_POLICY = 'USER_HAS_POLICY'
USER_HAS_POLICY_SUCCESS = 'User {} has policy {}'
USER_HAS_POLICY_FAIL = 'User {} is missing policy {}'

HAS_ACCESS_KEY = 'HAS_ACCESS_KEY'
HAS_ACCESS_KEY_SUCCESS = 'User {} has an active key'
HAS_ACCESS_KEY_FAIL = 'User {} should have an access key'

CONFIG_RULE_FOUND = 'CONFIG_RULE_FOUND'
CONFIG_RULE_FOUND_FAIL = 'Config rule {} not found'

CONFIG_RULE_ADDED = 'CONFIG_RULE_NOT_ADDED'
CONFIG_RULE_ADDED_FAIL = 'Unable to add config rule {} to account'
CONFIG_RULE_ADDED_SUCCESS = 'Config rule {} added to account'

NON_COMPLIANT_CONFIG = 'NON_COMPLIANT_CONFIG'
NON_COMPLIANT_CONFIG_FAIL = 'Config rule {} is non compliant'
NON_COMPLIANT_CONFIG_SUCCESS = 'Config rule {} is compliant'
NON_COMPLIANT_CONFIG_USER_FAIL = 'Config rule {} is non compliant for user {}'
NON_COMPLIANT_CONFIG_USER_SUCCESS = 'Config rule {} is compliant for user {}'
NON_COMPLIANT_CONFIG_S3_FAIL = 'Config rule {} is non compliant for bucket {}'
NON_COMPLIANT_CONFIG_S3_SUCCESS = 'Config rule {} is compliant for bucket {}'
NON_COMPLIANT_CONFIG_POLICY_FAIL = 'Config rule {} is non compliant for policy {}'
NON_COMPLIANT_CONFIG_POLICY_SUCCESS = 'Config rule {} is compliant for policy {}'

