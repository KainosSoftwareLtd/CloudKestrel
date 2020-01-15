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
SOURCEIPS = 'SourceIPs'

# "Policy": {
#     "Name": "User_Source_IP_Restrictions",
#     "Source_IPs": [
#         "195.89.171.5/32"
#     ]
# }

class UserSourceIPRestrictions(PolicyHelper):
    """A class to interrogate the correct setup of policy User_Source_IP_Restrictions"""

    policy_name = 'User_Source_IP_Restrictions'

    def __init__(self, session):
        self.session = session
        self.iam = session.client('iam')
        super().__init__(self.iam)

    def match(self, cloud, params):
        """
        A function to determine equality between the reference policy and the version in the target.
        :param cloud: The policy retrieved from the target
        :param params: The configurable params for the target.
        :return: A boolean.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = Path(dir_path)
        f = open(str(path.parent) + os.sep + 'Policies/User_Source_IP_Restrictions.json')
        ref_data = f.read()
        ref_json = json.loads(ref_data)
        ref_statement = ref_json['Statement']
        f.close()

        def parse_statement(data):
            """
            Parse the policy statement properties
            """
            effect = data[EFFECT]
            action = data[ACTION]
            resource = data[RESOURCE]
            sourceIPs = data['Condition']['NotIpAddress']['aws:SourceIp']

            return {EFFECT: effect, ACTION: action, RESOURCE: resource, SOURCEIPS: sourceIPs}

        def equals(ref, cloud, expected_source_ips):
            """
            Determine equality
            """

            fails = []
            if ref[EFFECT] != cloud[EFFECT]:
                fails.append('Effect doesn\'t match')
            if ref[ACTION] != cloud[ACTION]:
                fails.append('Action doesn\'t match')
            if ref[RESOURCE] != cloud[RESOURCE]:
                fails.append('Resource doesn\'t match')
            if expected_source_ips != cloud[SOURCEIPS]:
                fails.append('Source IPs don\'t match {} {}'.format(expected_source_ips, cloud[SOURCEIPS]))
            if fails:
                raise PolicyMatchException(self.policy_name, ','.join(fails))

            return ref[EFFECT] == cloud[EFFECT] and \
                ref[ACTION] == cloud[ACTION] and \
                ref[RESOURCE] == cloud[RESOURCE] and \
                expected_source_ips == cloud[SOURCEIPS]

        ref_attribs = parse_statement(ref_statement)
        cloud_attribs = parse_statement(cloud)

        return equals(ref_attribs, cloud_attribs, params)

    def hunt(self, rule):
        """
        Hunt for the correct setup of this policy and whether its set for all users.
        """

        results = []

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
            self.match(document, rule['Source_IPs'])
        except PolicyMatchException as pme:
            results.append(pme.to_result())
        else:
            results.append(Result(codes.POLICY_MATCH, True, codes.POLICY_MATCH_SUCCESS.format(self.policy_name)))

        # Test every user has the Policy
        users = self.list_users()
        for user in users:
            user_name = user['UserName']
            has_policy = self.user_has_policy(user_name, 'User_Source_IP_Restrictions')
            if has_policy:
                results.append(Result(codes.USER_HAS_POLICY, True, codes.USER_HAS_POLICY_SUCCESS.format(user_name, self.policy_name)))
            else:
                results.append(Result(codes.USER_HAS_POLICY, False, codes.USER_HAS_POLICY_FAIL.format(user_name, self.policy_name)))

        return results
