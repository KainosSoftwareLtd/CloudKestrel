# CloudKestrel

A project to audit the security of AWS accounts.

## Targets

AWS accounts to audit are defined in targets.json.  
A target account details the environmental variable names of the AWS Access Key and AWS Secret Access Key.
Environment variables with names detailed in targets.json should be available to the running script. 

The target also details the rules to run against the target which are AWS policies or AWS configs.

```json
{
  "Targets": [{
      "target1": {
        "Credentials": {
          "AwsAccessKeyId": "TARGET1_AWS_ACCESS_KEY_ID",
          "AwsSecretAccessKey": "TARGET1_AWS_SECRET_ACCESS_KEY"
        },
        "Rules": [{
          "Policy": {
            "Name": "User_Source_IP_Restrictions",
            "Params": [{
              "PARAM_1_SOURCE_IP": ["195.89.85.67"]
            }]}
        }]
      }
    }
  ]
}
```

## Reference Policies

Reference policies are stored in the Polices directory.  These detail the policies that should exist in the target with templated paramaters that allow every target to have specific values.

## Results

The audit results are produced in the form of a JSON string and are also written to an html report.
The main script cloudkestrel.py return 0 if all tests pass and non zero if any test fails.

## Sample Report
![Sample Report](sample_report.png)

## Dependencies
pip3 install boto3

## Get Started
python3 cloudkestrel.py