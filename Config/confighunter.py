import logging

from Config.IamRootAccessKeyCheck import IamRootAccessKeyCheck
from Config.IamUserMfaEnabled import IamUserMfaEnabled
from Config.IamUserUnusedCredentialsCheck import IamUserUnusedCredentialsCheck
from Config.IamUserNoPoliciesCheck import IamUserNoPoliciesCheck
from Config.IamPolicyNoStatementsWithAdminAccess import IamPolicyNoStatementsWithAdminAccess
from Config.IamUserGroupMembershipCheck import IamUserGroupMembershipCheck
from Config.S3BucketPublicReadProhibited import S3BucketPublicReadProhibited
from Config.S3BucketPublicWriteProhibited import S3BucketPublicWriteProhibited

logger = logging.getLogger('cloudkestrel')


def store_results(config_result, config_name, results):
    config_result['ConfigResult']['ConfigName'] = config_name
    config_result['ConfigResult']['Results'] = results


def hunt_config(config, session):
    """
    A function that knows how to interrogate a target for a given config.
    :param config: A config name and parameters.
    :param session: A boto Session.
    :return: The config result in the form of a dict.
    e.g. {'ConfigResult': {'ConfigName': 'Some Config', 'Results': []}}
    """
    name = config['Name']
    logger.info('Hunting for config rule %s', name)
    config_result = {'ConfigResult': {}}
    if name == 'IAM_ROOT_ACCESS_KEY_CHECK':
        iam_root_access_key_check = IamRootAccessKeyCheck(session)
        results = iam_root_access_key_check.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'IAM_USER_MFA_ENABLED':
        iam_user_mfa_enabled = IamUserMfaEnabled(session)
        results = iam_user_mfa_enabled.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'IAM_USER_UNUSED_CREDENTIALS_CHECK':
        iam_user_unused_credentials_check = IamUserUnusedCredentialsCheck(session)
        results = iam_user_unused_credentials_check.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'S3_BUCKET_PUBLIC_READ_PROHIBITED':
        s3_bucket_public_read_prohibited = S3BucketPublicReadProhibited(session)
        results = s3_bucket_public_read_prohibited.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'S3_BUCKET_PUBLIC_WRITE_PROHIBITED':
        s3_bucket_public_write_prohibited = S3BucketPublicWriteProhibited(session)
        results = s3_bucket_public_write_prohibited.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'IAM_USER_NO_POLICIES_CHECK':
        iam_user_no_policies_check = IamUserNoPoliciesCheck(session)
        results = iam_user_no_policies_check.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS':
        iam_policy_no_statements_with_admin_access = IamPolicyNoStatementsWithAdminAccess(session)
        results = iam_policy_no_statements_with_admin_access.hunt(config)
        store_results(config_result, name, results)
        return config_result
    elif name == 'IAM_USER_GROUP_MEMBERSHIP_CHECK':
        iam_user_group_membership_check = IamUserGroupMembershipCheck(session)
        results = iam_user_group_membership_check.hunt(config)
        store_results(config_result, name, results)
        return config_result

