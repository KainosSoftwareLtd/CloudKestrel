import datetime
import json
import os
from string import Template


class Reporter:

    def __init__(self, data):
        self.data = json.loads(data)

    def construct_html_from_results(self, results):
        lines = []
        for result in results:
            code = result['code']
            outcome = result['outcome']
            if not outcome:
                row_class = 'class="table-danger"'
            else:
                row_class = 'class="table-success"'
            desc = result['desc']

            line = '<tr {}><td>{}</td><td>{}</td></tr>'.format(row_class, code, desc)
            lines.append(line)

        return ''.join(lines)

    def construct_policy_result(self, rule_result):
        policy_name = rule_result['Result']['PolicyResult']['PolicyName']
        results = rule_result['Result']['PolicyResult']['Results']
        html_results = self.construct_html_from_results(results)

        template = self.get_template('policy.html')
        return template.substitute(policy_name=policy_name, policy_results=html_results)

    def construct_config_result(self, rule_result):
        config_name = rule_result['Result']['ConfigResult']['ConfigName']
        results = rule_result['Result']['ConfigResult']['Results']
        html_results = self.construct_html_from_results(results)

        template = self.get_template('config.html')
        return template.substitute(config_name=config_name, config_results=html_results)

    def construct_rule_results(self):
        policies = []
        configs = []
        rule_results = self.data['TargetResult']['RuleResults']
        for rule_result in rule_results:
            type = rule_result['Type']
            if type == 'Policy':
                policies.append(self.construct_policy_result(rule_result))
            elif type == 'Config':
                configs.append(self.construct_config_result(rule_result))

        return policies, configs

    def get_template(self, file_name):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        template_file = open(__location__ + os.sep + file_name)
        template_data = template_file.read()
        return Template(template_data)

    def report(self):
        # print(json.dumps(self.data))

        target_name = self.data['TargetResult']['Target']
        date = datetime.date.today()
        date_string = date.strftime("%b %d %Y %H:%M:%S")

        policies, configs = self.construct_rule_results()

        policies_html = '</br>'.join(policies)
        configs_html = '</br>'.join(configs)

        template = self.get_template('template.html')
        output = (template.substitute(target=target_name, date=date_string, policies=policies_html, configs=configs_html))

        # Docker host_dir env variable, if we are not in Docker just write it to the cd
        host_dir = os.getenv('HOST_DIR', '')
        if host_dir:
            host_dir = host_dir + os.sep

        f = open(host_dir + target_name + '.html', "w+")
        f.write(output)

    def get_all_results(self):
        all_results = []
        rule_results = self.data['TargetResult']['RuleResults']
        for rule_result in rule_results:
            type = rule_result['Type']
            if type == 'Policy':
                all_results.extend(rule_result['Result']['PolicyResult']['Results'])
            elif type == 'Config':
                all_results.extend(rule_result['Result']['ConfigResult']['Results'])
        return all_results

    def outcome(self):
        all_results = self.get_all_results()
        for result in all_results:
            if result['outcome'] is False:
                return 1
        return 0

