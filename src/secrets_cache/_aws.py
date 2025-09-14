"""AWS module."""
from json import loads

import boto3
from botocore.exceptions import ClientError

from ._cache import cached_fetch
from ._constants import DEFAULT_CACHE_TTL, DEFAULT_AWS_REGION

# Module-level caches
_boto_clients = {}


def get_boto_client(service: str, region: str):
    """Cache boto3 clients per service/region."""
    key = service, region
    _client = _boto_clients.get(key)
    if _client is None:
        _boto_clients[key] = _client = boto3.client(service, region_name=region)
    return _client


def get_secret(name: str,
               region: str = DEFAULT_AWS_REGION,
               ttl: int = DEFAULT_CACHE_TTL,
               force_refresh: bool = False,
               raw: bool = False) -> str | bytes | dict:
    """Get secret from AWS Secrets Manager with optional caching."""
    value = cached_fetch('secretsmanager', name, region, _fetch_secret, ttl, force_refresh)

    if raw:
        return value

    # Try to parse JSON (most Secrets Manager use case)
    try:
        return loads(value)
    except (ValueError, TypeError):
        return value


def get_param(name: str,
              region: str = DEFAULT_AWS_REGION,
              ttl: int = DEFAULT_CACHE_TTL,
              force_refresh: bool = False) -> str:
    """Get parameter from AWS SSM Parameter Store with optional caching."""
    return cached_fetch('ssm', name, region, _fetch_param, ttl, force_refresh)


def _fetch_secret(name: str, region: str) -> str | bytes | None:
    client = get_boto_client('secretsmanager', region)

    try:
        resp = client.get_secret_value(
            SecretId=name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        err_code = e.response['Error']['Code']
        if err_code == 'ResourceNotFoundException':
            print(f'The requested secret {name} was not found')
        elif err_code == 'InvalidRequestException':
            print('The request was invalid due to:', e)
        elif err_code == 'InvalidParameterException':
            print('The request had invalid params:', e)
        elif err_code == 'DecryptionFailure':
            print('The requested secret can\'t be decrypted using the provided KMS key:', e)
        elif err_code == 'InternalServiceError':
            print('An error occurred on service side:', e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if (secret := resp.get('SecretString')) is not None:
            return secret
        return resp['SecretBinary']


def _fetch_param(name: str, region: str):
    client = get_boto_client('ssm', region)

    resp = client.get_parameter(Name=name, WithDecryption=True)

    param = resp['Parameter']['Value']
    return param
