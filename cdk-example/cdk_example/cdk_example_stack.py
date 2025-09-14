from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_ssm as ssm,
)


class CdkExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Secrets Manager secret for testing
        test_secret = secretsmanager.Secret(
            self, "TestSecret",
            secret_name="my-test-secret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"user","password":"pass"}',
                generate_string_key="token"
            )
        )

        # Create a Parameter Store entry
        test_param = ssm.StringParameter(
            self, "TestParam",
            parameter_name="/my/test/param",
            string_value="hello-world"
        )

        # Lambda function
        test_lambda = _lambda.Function(
            self, "TestLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.handler",  # function inside your lambda file
            code=_lambda.Code.from_asset(
                path="lambda",
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_12.bundling_image,
                    "command": ["bash", "-c",
                                "pip install -r requirements.txt -t /asset-output && find /asset-output -name '*.dist-info' -type d -exec rm -rf {} + && cp -r . /asset-output"],
                }
            ),
            environment={
                "TEST_SECRET_NAME": test_secret.secret_name,
                "TEST_PARAM_NAME": test_param.parameter_name
            },
        )

        # Grant Lambda permissions to read secret & parameter
        test_secret.grant_read(test_lambda)
        test_param.grant_read(test_lambda)
