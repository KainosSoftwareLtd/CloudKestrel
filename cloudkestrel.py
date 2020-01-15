import json
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError

from Config.confighunter import *
from Policy.policyhunter import *
from Exceptions.CredentialsException import CredentialsException
from Exceptions.EnvironmentVariableException import EnvironmentVariableException
from Report.Reporter import Reporter
from Result import CustomEncoder

CREDENTIALS = 'Credentials'
TARGETRESULT = 'TargetResult'
RULERESULTS = 'RuleResults'


logger = logging.getLogger('cloudkestrel')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def load_session(target):
    """
    Creates a boto Session.
    :param target: The AWS target that is to be audited.  This target contains environmental variables names that
    represent the AWS Access Key ID and the AWS Secret Access Key.
    :return: A boto Session.
    """
    target_name = list(target.keys())[0]
    envAwsAccessKeyId = target[target_name][CREDENTIALS]['AwsAccessKeyId']
    envAwsSecretAccessKey = target[target_name][CREDENTIALS]['AwsSecretAccessKey']

    try:
        access_key = os.environ[envAwsAccessKeyId]
    except KeyError:
        logging.exception('Environment variable for %s is missing', envAwsAccessKeyId)
        raise EnvironmentVariableException(envAwsAccessKeyId, target_name)

    try:
        secret_key = os.environ[envAwsSecretAccessKey]
    except KeyError:
        logging.exception('Environment variable for %s is missing', envAwsSecretAccessKey)
        raise EnvironmentVariableException(envAwsSecretAccessKey, target_name)

    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )


def test_session(session, target_name):
    iam = session.client('iam')

    try:
        iam.list_users()
        logger.info('Session for target: %s is valid', target_name)
    except ClientError as ex:
        logger.error('Session for target: %s is invalid', target_name)
        raise CredentialsException(str(ex))


def process_rule(rule, session):
    """
    Executes a rule which represents some form of audit on the AWS target.
    :param rule: The rule to process.
    :param session: The boto Session.
    :return: The result in the form of a dict.
    e.g. {'Type': 'Policy', 'Result': {}}
    """
    rule_result = {}

    rule_type = list(rule.keys())[0]
    if rule_type == 'Policy':
        policy_result = hunt_policy(rule[rule_type], session)
        rule_result['Type'] = 'Policy'
        rule_result['Result'] = policy_result
    elif rule_type == 'Config':
        rule_results = hunt_config(rule[rule_type], session)
        rule_result['Type'] = 'Config'
        rule_result['Result'] = rule_results

    return rule_result


def process_rules(target):
    """
    Process all rules for a given target.
    :param target: The AWS target and all its rules.
    :return: The result in the form of a dict.
    e.g. {'TargetResult': {'Target': 'Some Target', 'RuleResults': []}}
    """
    target_name = list(target.keys())[0]
    rules = target[target_name]['Rules']
    target_result = {TARGETRESULT: {'Target': target_name, RULERESULTS: []}}

    try:
        session = load_session(target)
    except EnvironmentVariableException as eve:
        logger.exception('Session variables are not valid')
        target_result[TARGETRESULT]['Failure'] = eve.desc
        return target_result

    try:
        test_session(session, target_name)
    except CredentialsException as ce:
        logger.exception('Session is not valid')
        target_result[TARGETRESULT]['Failure'] = ce.desc
        return target_result

    for rule in rules:
        rule_result = process_rule(rule, session)
        rules_results = target_result[TARGETRESULT][RULERESULTS]
        rules_results.append(rule_result)
        target_result[TARGETRESULT][RULERESULTS] = rules_results

    return target_result


def load_targets():
    """
    Load all the targets from the targets.json file.
    :return: All the results in the form of a list.
    """
    target_results = []
    f = open(os.getcwd() + os.sep + 'targets.json')
    target_data = f.read()
    target_json = json.loads(target_data)
    targets = target_json['Targets']
    for target in targets:
        rules_results = process_rules(target)
        target_results.append(rules_results)

    return target_results


# Load all targets and execute
results = load_targets()
return_code = 0
for result in results:
    reporter = Reporter(json.dumps(result, cls=CustomEncoder))
    reporter.report()
    return_code = return_code + reporter.outcome()

sys.exit(return_code)