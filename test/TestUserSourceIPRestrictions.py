import unittest
from unittest.mock import MagicMock

import codes
from Exceptions.PolicyMatchException import PolicyMatchException
from Policy.UserSourceIPRestrictions import UserSourceIPRestrictions


class TestUserSourceIPRestrictions(unittest.TestCase):

    def test_match(self):
        cloud_policy = {'Effect': 'Deny', 'Action': '*', 'Resource': '*', 'Condition': {'NotIpAddress': {'aws:SourceIp': ['195.89.171.5/32']}}}
        params = ['195.89.171.5/32']

        # Setup Mock
        session = MagicMock()
        session.client.return_value = None

        # Call and test
        match = UserSourceIPRestrictions(session).match(cloud_policy, params)
        self.assertEqual(match, True)

    def test_non_match(self):
        cloud_policy = {'Effect': 'Deny', 'Action': '*', 'Resource': '*', 'Condition': {'NotIpAddress': {'aws:SourceIp': ['195.89.171.5/32']}}}
        params = ['1.1.1.1/32']

        # Setup Mock
        session = MagicMock()
        session.client.return_value = None

        # Call and test
        try:
            UserSourceIPRestrictions(session).match(cloud_policy, params)
        except PolicyMatchException as pme:
            self.assertEqual(pme.code, codes.POLICY_MATCH)

