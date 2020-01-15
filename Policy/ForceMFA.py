import json
import os
from pathlib import Path

import codes
from Exceptions.PolicyMatchException import PolicyMatchException
from Exceptions.PolicyNotFoundException import PolicyNotFoundException
from Result import Result
from .PolicyHelper import PolicyHelper

EFFECT = 'Effect'
ACTION = 'Action'
RESOURCE = 'Resource'

# "Policy": {
#     "Name": "Force_MFA",
#     "IgnoreUsers": ["SecurityReader"]
# }

class ForceMFA(PolicyHelper):
    """A class to interrogate the correct setup of policy Force_MFA"""

    policy_name = 'Force_MFA'

    def __init__(self, session):
        self.session = session
        self.iam = session.client('iam')
        super().__init__(self.iam)

    def match(self, cloud):
        """
        A function to determine equality between the reference policy and the version in the target.
        :param cloud: The policy retrieved from the target
        :return: A boolean.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = Path(dir_path)
        f = open(str(path.parent) + os.sep + 'Policies/Force_MFA.json')
        ref_data = f.read()
        ref_json = json.loads(ref_data)
        ref_statement = ref_json['Statement']
        f.close()

        if ref_statement != cloud:
            raise PolicyMatchException(self.policy_name, 'Policy text doesn\'t match')

    def hunt(self, rule):
        """
        Hunt for the correct setup of this policy and whether its set for all users.
        """

        results = []

        ignore_users = rule['IgnoreUsers']

        # Find policy
        arn, version_id = None, None
        try:
            arn, version_id = self.find_policy(self.policy_name)
        except PolicyNotFoundException as pnfe:
            results.append(pnfe.to_result())
        else:
            results.append(Result(codes.POLICY_FOUND, True, codes.POLICY_FOUND_SUCCESS.format(self.policy_name)))

        # Get Document and test it for equality
        document = self.get_policy_document(arn, version_id)
        try:
            self.match(document)
        except PolicyMatchException as pme:
            results.append(pme.to_result())
        else:
            results.append(Result(codes.POLICY_MATCH, True, codes.POLICY_MATCH_SUCCESS.format(self.policy_name)))

        # Test every user has the Policy
        users = self.list_users()
        for user in users:
            user_name = user['UserName']
            if user_name not in ignore_users:
                has_policy = self.user_has_policy(user_name, 'Force_MFA')
                if has_policy:
                    results.append(Result(codes.USER_HAS_POLICY, True, codes.USER_HAS_POLICY_SUCCESS.format(user_name, self.policy_name)))
                else:
                    results.append(Result(codes.USER_HAS_POLICY, False, codes.USER_HAS_POLICY_FAIL.format(user_name, self.policy_name)))

        return results
