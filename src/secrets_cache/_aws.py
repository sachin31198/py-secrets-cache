"""AWS module."""
from json import loads

import boto3

from ._cache import cached_fetch
from ._constants import DEFAULT_CACHE_TTL


# Module-level caches
_boto_clients = {}


def get_boto_client(service: str, region: str = 'us-east-1'):
    """Cache boto3 clients per service/region."""
    key = service, region
    _client = _boto_clients.get(key)
    if _client is None:
        _boto_clients[key] = _client = boto3.client(service, region_name=region)
    return _client


def get_secret(name: str,
               region: str = 'us-east-1',
               ttl: int = DEFAULT_CACHE_TTL,
               force_refresh: bool = False,
               raw: bool = False):
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
              region: str = 'us-east-1',
              ttl: int = DEFAULT_CACHE_TTL,
              force_refresh: bool = False):
    """Get parameter from AWS SSM Parameter Store with optional caching."""
    return cached_fetch('ssm', name, region, _fetch_param, ttl, force_refresh)


def _fetch_secret(name: str, region: str = 'us-east-1'):
    client = get_boto_client('secretsmanager', region)
    resp = client.get_secret_value(SecretId=name)
    return resp['SecretString']


def _fetch_param(name: str, region: str = 'us-east-1'):
    client = get_boto_client('ssm', region)
    resp = client.get_parameter(Name=name, WithDecryption=True)
    return resp['Parameter']['Value']
