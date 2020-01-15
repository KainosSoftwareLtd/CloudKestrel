import logging

from Exceptions.PolicyNotFoundException import PolicyNotFoundException

logger = logging.getLogger('cloudkestrel')


class PolicyHelper:
    """
    A class that provides base Policy helpers.
    """

    def __init__(self, iam):
        self.iam = iam

    def get_policy_document(self, arn, versionId):
        """
        Gets a policy document.
        :param arn: The Policy ARN.
        :param versionId: The Policy version id.
        :return: The contents of the Policy.
        """
        logger.info('Getting policy document')
        response = self.iam.get_policy_version(PolicyArn=arn, VersionId=versionId)
        return response['PolicyVersion']['Document']['Statement']

    def find_policy(self, policy_name):
        """
        Finds a given policy by name.
        :param policy_name: The name of the policy.
        :return: arn, versionId tuple.
        """
        logger.info('Finding policy %s', policy_name)
        arn = None
        versionId = None
        response = self.iam.list_policies(Scope='Local')
        policies = response['Policies']
        for policy in policies:
            if policy['PolicyName'] == policy_name:
                arn = policy['Arn']
                versionId = policy['DefaultVersionId']
                break

        if arn is None:
            logger.exception('Policy %s not found', policy_name)
            raise PolicyNotFoundException(policy_name)

        return arn, versionId

    def list_users(self):
        """
        Lists all the users of a target.
        :return: The users.
        """
        r = self.iam.list_users()
        return r['Users']

    def list_groups_for_user(self, user_name):
        """
        Get the groups of a user.
        :param user_name: The user name.
        :return: The groups.
        """
        r = self.iam.list_groups_for_user(UserName=user_name)
        groups = r['Groups']
        return groups

    def policy_names_for_group(self, group_name):
        """
        Get the attached policies for a group.
        :param group_name: The group name.
        :return: The policy names.
        """
        r = self.iam.list_attached_group_policies(GroupName=group_name)
        attached_policies = r['AttachedPolicies']
        policy_names = []
        for attached_policy in attached_policies:
            policy_names.append(attached_policy['PolicyName'])
        return policy_names

    def user_has_policy(self, user_name, policy_name):
        """
        Has a given user got a given policy.
        :param user_name: The user name.
        :param policy_name: The policy name.
        :return:
        """
        logger.info('Determining if user %s has policy %s', user_name, policy_name)
        has_policy = False
        groups = self.list_groups_for_user(user_name)
        for group in groups:
            group_name = group['GroupName']
            policy_names = self.policy_names_for_group(group_name)
            for found_policy_name in policy_names:
                if found_policy_name == policy_name:
                    has_policy = True
        return has_policy
