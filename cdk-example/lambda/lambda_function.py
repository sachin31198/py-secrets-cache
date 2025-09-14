# lambda_function.py
import os
from secrets_cache import get_secret, get_param

def handler(event, context):
    # Example usage
    secret_name = os.getenv("TEST_SECRET_NAME", "my-test-secret")
    param_name = os.getenv("TEST_PARAM_NAME", "/my/test/param")

    secret = get_secret(secret_name)
    param = get_param(param_name)

    return {
        "secret": secret,
        "param": param
    }
