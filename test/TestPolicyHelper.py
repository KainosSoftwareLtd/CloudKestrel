import unittest
from unittest.mock import MagicMock

from Policy.PolicyHelper import PolicyHelper


class TestPolicyHelper(unittest.TestCase):

    test_get_policy_document_response = {'PolicyVersion': {'Document': {'Version': '2012-10-17', 'Statement': {'Effect': 'Deny', 'Action': '*', 'Resource': '*', 'Condition': {'NotIpAddress': {'aws:SourceIp': ['195.89.171.5/32']}}}}, 'VersionId': 'v1', 'IsDefaultVersion': True}, 'ResponseMetadata': {'RequestId': 'c38cc0c4-886e-44dc-9c80-fa6b6fe868cb', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'c38cc0c4-886e-44dc-9c80-fa6b6fe868cb', 'content-type': 'text/xml', 'content-length': '1212', 'date': 'Tue, 05 Nov 2019 13:30:46 GMT'}, 'RetryAttempts': 0}}
    test_get_policy = {'Effect': 'Deny', 'Action': '*', 'Resource': '*', 'Condition': {'NotIpAddress': {'aws:SourceIp': ['195.89.171.5/32']}}}
    test_list_policies = {'Policies': [{'PolicyName': 'User_Source_IP_Restrictions', 'PolicyId': 'ANPA4EXDCA6US3CTMMR6K', 'Arn': 'arn:aws:iam::834773583785:policy/User_Source_IP_Restrictions', 'Path': '/', 'DefaultVersionId': 'v1', 'AttachmentCount': 1, 'PermissionsBoundaryUsageCount': 0, 'IsAttachable': True}], 'IsTruncated': False, 'ResponseMetadata': {'RequestId': '4df66645-0e2a-4ee8-8873-620d02036fb5', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '4df66645-0e2a-4ee8-8873-620d02036fb5', 'content-type': 'text/xml', 'content-length': '1431', 'date': 'Tue, 05 Nov 2019 14:31:57 GMT'}, 'RetryAttempts': 0}}
    test_list_users_response = {'Users': [{'Path': '/', 'UserName': 'billy', 'UserId': 'AIDA4EXDCA6U4UMFOFVK4', 'Arn': 'arn:aws:iam::834773583785:user/billy'}], 'IsTruncated': False, 'ResponseMetadata': {'RequestId': '5536b869-2887-402f-9da8-ac69cb5a58ff', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '5536b869-2887-402f-9da8-ac69cb5a58ff', 'content-type': 'text/xml', 'content-length': '1443', 'date': 'Tue, 05 Nov 2019 14:51:49 GMT'}, 'RetryAttempts': 0}}
    test_groups_for_user_response = {'Groups': [{'Path': '/', 'GroupName': 'MyS3Users', 'GroupId': 'AGPA4EXDCA6UU6CP36JTV', 'Arn': 'arn:aws:iam::834773583785:group/MyS3Users'}], 'IsTruncated': False, 'ResponseMetadata': {'RequestId': '053a17dd-b1a1-4c85-92dd-38b315241b13', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '053a17dd-b1a1-4c85-92dd-38b315241b13', 'content-type': 'text/xml', 'content-length': '594', 'date': 'Tue, 05 Nov 2019 15:56:28 GMT'}, 'RetryAttempts': 0}}
    test_attached_group_policies = {'AttachedPolicies': [{'PolicyName': 'User_Source_IP_Restrictions', 'PolicyArn': 'arn:aws:iam::834773583785:policy/User_Source_IP_Restrictions'}, {'PolicyName': 'AmazonVPCFullAccess', 'PolicyArn': 'arn:aws:iam::aws:policy/AmazonVPCFullAccess'}], 'IsTruncated': False, 'ResponseMetadata': {'RequestId': 'cbdf6938-f2b4-4528-9db3-6b15dfd273ad', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'cbdf6938-f2b4-4528-9db3-6b15dfd273ad', 'content-type': 'text/xml', 'content-length': '730', 'date': 'Tue, 05 Nov 2019 16:45:12 GMT'}, 'RetryAttempts': 0}}

    def test_get_policy_document(self):
        # Setup Mock
        iam = MagicMock()
        iam.get_policy_version.return_value = self.test_get_policy_document_response

        # Call and test
        document = PolicyHelper(iam).get_policy_document(None, None)
        self.assertEqual(document, self.test_get_policy)

    def test_find_policy(self):
        # Setup Mock
        iam = MagicMock()
        iam.list_policies.return_value = self.test_list_policies

        # Call and test
        arn, versionId = PolicyHelper(iam).find_policy('User_Source_IP_Restrictions')
        self.assertEqual(arn, 'arn:aws:iam::834773583785:policy/User_Source_IP_Restrictions')
        self.assertEqual(versionId, 'v1')

    def test_list_users(self):
        # Setup Mock
        iam = MagicMock()
        iam.list_users.return_value = self.test_list_users_response

        # Call and test
        users = PolicyHelper(iam).list_users()
        user_name = users[0]['UserName']
        self.assertEqual(len(users), 1)
        self.assertEqual(user_name, 'billy')

    def test_list_groups_for_user(self):
        # Setup Mock
        iam = MagicMock()
        iam.list_groups_for_user.return_value = self.test_groups_for_user_response

        # Call and test
        groups = PolicyHelper(iam).list_groups_for_user('some_user')
        group_name = groups[0]['GroupName']
        self.assertEqual(len(groups), 1)
        self.assertEqual(group_name, 'MyS3Users')

    def test_policy_names_for_group(self):
        # Setup Mock
        iam = MagicMock()
        iam.list_attached_group_policies.return_value = self.test_attached_group_policies

        # Call and test
        attached_policies = PolicyHelper(iam).policy_names_for_group('some_group')
        policy_name = attached_policies[0]
        self.assertEqual(len(attached_policies), 2)
        self.assertEqual(policy_name, 'User_Source_IP_Restrictions')

    def test_user_has_policy(self):
        # Setup Mock
        iam = MagicMock()
        iam.list_groups_for_user.return_value = self.test_groups_for_user_response
        iam.list_attached_group_policies.return_value = self.test_attached_group_policies

        # Call and test
        has_policy = PolicyHelper(iam).user_has_policy('', 'User_Source_IP_Restrictions')
        self.assertEqual(has_policy, True)

