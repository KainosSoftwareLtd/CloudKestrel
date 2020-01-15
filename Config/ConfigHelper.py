import logging

from botocore.exceptions import ClientError

import codes
from Exceptions.ConfigRuleNotFoundException import ConfigRuleNotFoundException
from Exceptions.ConfigRuleNotAddedException import ConfigRuleNotAddedException
from Result import Result

logger = logging.getLogger('cloudkestrel')


class ConfigHelper:
    """
    A class that provides base Config helpers.
    """

    def __init__(self, config):
        self.config = config

    def get_compliance_for_rule(self, rule_name):
        try:
            logger.info('Get compliance for rule %s', rule_name)
            r = self.config.get_compliance_details_by_config_rule(ConfigRuleName=rule_name)
            compliance_data = []
            compliance_results = r['EvaluationResults']
            for compliance_result in compliance_results:
                compliance = compliance_result['ComplianceType']
                qualifier = compliance_result['EvaluationResultIdentifier']['EvaluationResultQualifier']
                compliance_data.append({'compliance': compliance, 'qualifier': qualifier})
            return compliance_data
        except ClientError as ce:
            logger.exception('Failure getting compliance for rule %s', rule_name)
            if 'NoSuchConfigRuleException' in str(ce):
                raise ConfigRuleNotFoundException(rule_name)
            else:
                raise ce

    def add_config_rule(self, rule):
        try:
            self.config.put_config_rule(ConfigRule=rule)
            return Result(codes.CONFIG_RULE_ADDED, True, codes.CONFIG_RULE_ADDED_SUCCESS.format(self.rule_name))
        except ClientError as ce:
            logger.exception('Failed to add config rule name %s', self.rule_name)
            raise ConfigRuleNotAddedException(self.rule_name)

    def get_resource(self, resource_type, resource_id):
        r = self.config.batch_get_resource_config(
            resourceKeys=[
                {
                    'resourceType': resource_type,
                    'resourceId': resource_id
                },
            ]
        )
        if len(r['baseConfigurationItems']) == 0:
            return 'Unknown Resource'
        else:
            return r['baseConfigurationItems'][0]['resourceName']

    def hunt(self, config):
        add_if_missing = config['AddIfMissing']
        ignore_users = config.get('IgnoreUsers', [])
        results = []

        try:
            compliance_results = self.get_compliance_for_rule(self.rule_name.lower())
        except ConfigRuleNotFoundException as crnfe:
            results.append(crnfe.to_result())
            try:
                if add_if_missing:
                    results.append(self.add())
            except ConfigRuleNotAddedException as crnae:
                results.append(crnae.to_result())
            return results

        for compliance_result in compliance_results:
            resource_type = compliance_result['qualifier']['ResourceType']
            resource_id = compliance_result['qualifier']['ResourceId']

            if 'User' in resource_type:
                resource_name = self.get_resource(resource_type, resource_id)
                if resource_name in ignore_users:
                    continue
                success = codes.NON_COMPLIANT_CONFIG_USER_SUCCESS.format(self.rule_name, resource_name)
                fail = codes.NON_COMPLIANT_CONFIG_USER_FAIL.format(self.rule_name, resource_name)
            elif 'S3' in resource_type:
                resource_name = self.get_resource(resource_type, resource_id)
                success = codes.NON_COMPLIANT_CONFIG_S3_SUCCESS.format(self.rule_name, resource_name)
                fail = codes.NON_COMPLIANT_CONFIG_S3_FAIL.format(self.rule_name, resource_name)
            elif 'Policy' in resource_type:
                resource_name = self.get_resource(resource_type, resource_id)
                success = codes.NON_COMPLIANT_CONFIG_POLICY_SUCCESS.format(self.rule_name, resource_name)
                fail = codes.NON_COMPLIANT_CONFIG_POLICY_FAIL.format(self.rule_name, resource_name)
            else:
                success = codes.NON_COMPLIANT_CONFIG_SUCCESS.format(self.rule_name)
                fail = codes.NON_COMPLIANT_CONFIG_FAIL.format(self.rule_name)

            if compliance_result['compliance'] == 'COMPLIANT':
                results.append(Result(codes.NON_COMPLIANT_CONFIG, True, success))
            else:
                results.append(Result(codes.NON_COMPLIANT_CONFIG, False, fail))

        return results
