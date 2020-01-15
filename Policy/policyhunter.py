import logging

from Policy.UserSourceIPRestrictions import UserSourceIPRestrictions
from Policy.ForceMFA import ForceMFA

logger = logging.getLogger('cloudkestrel')


def hunt_policy(policy, session):
    """
    A function that knows how to interrogate a target for a given policy.
    :param policy: A policy name and parameters.
    :param session: A boto Session.
    :return: The policy result in the form of a dict.
    e.g. {'PolicyResult': {'PolicyName': 'Some Policy', 'Results': []}}
    """
    name = policy['Name']
    policy_result = {'PolicyResult': {}}
    if name == 'User_Source_IP_Restrictions':
        logger.info('Hunting for policy User_Source_IP_Restrictions')
        user_source_ip_restrictions = UserSourceIPRestrictions(session)
        results = user_source_ip_restrictions.hunt(policy)
        policy_result['PolicyResult']['PolicyName'] = name
        policy_result['PolicyResult']['Results'] = results
        return policy_result
    elif name == 'Force_MFA':
        logger.info('Hunting for policy Force_MFA')
        force_MFA = ForceMFA(session)
        results = force_MFA.hunt(policy)
        policy_result['PolicyResult']['PolicyName'] = name
        policy_result['PolicyResult']['Results'] = results
        return policy_result
