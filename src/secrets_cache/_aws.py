"""Main module."""

from pathlib import Path

import boto3

from ._cache import cached_fetch


# Optional: import TOML only if available
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Python 3.10
    except ImportError:
        tomllib = None

try:
    import tomli_w
except ImportError:
    tomli_w = None


# Module-level caches
_secret_cache = {}
_param_cache = {}
_boto_clients = {}

# TOML cache file (optional)
_CACHE_FILE = Path.home() / '.secrets_cache.toml'


def get_boto_client(service: str, region: str = 'us-east-1'):
    """Cache boto3 clients per service/region."""
    key = service, region
    _client = _boto_clients.get(key)
    if _client is None:
        _boto_clients[key] = _client = boto3.client(service, region_name=region)
    return _client


def _read_toml_cache():
    if not tomllib or not _CACHE_FILE.exists():
        return {}
    with _CACHE_FILE.open('rb') as f:
        return tomllib.load(f)


def _write_toml_cache(data):
    if not tomli_w or not _CACHE_FILE.parent.exists():
        return
    with _CACHE_FILE.open('wb') as f:
        tomli_w.dump(data, f)


def get_secret(name: str, region: str = 'us-east-1', ttl: int = 7 * 24 * 3600):
    """Get secret from AWS Secrets Manager with optional caching."""
    return cached_fetch(_secret_cache, name, region, _fetch_secret, ttl)


def get_param(name: str, region: str = 'us-east-1', ttl: int = 7 * 24 * 3600):
    """Get parameter from AWS SSM Parameter Store with optional caching."""
    return cached_fetch(_param_cache, name, region, _fetch_param, ttl)


def _fetch_secret(name: str, region: str = 'us-east-1'):
    client = get_boto_client('secretsmanager', region)
    resp = client.get_secret_value(SecretId=name)
    value = resp['SecretString']

    # Update local TOML cache if available
    data = _read_toml_cache()
    data[name] = value
    _write_toml_cache(data)
    return value


def _fetch_param(name: str, region: str = 'us-east-1'):
    client = get_boto_client('ssm', region)
    resp = client.get_parameter(Name=name, WithDecryption=True)
    value = resp['Parameter']['Value']

    # Update local TOML cache if available
    data = _read_toml_cache()
    data[name] = value
    _write_toml_cache(data)
    return value
