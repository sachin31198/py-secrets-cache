# Secrets Cache

[![PyPI version](https://img.shields.io/pypi/v/secrets-cache.svg)](https://pypi.org/project/secrets-cache/)
[![PyPI license](https://img.shields.io/pypi/l/secrets-cache.svg)](https://pypi.org/project/secrets-cache/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/secrets-cache.svg)](https://pypi.org/project/secrets-cache/)
[![GitHub Actions](https://github.com/rnag/py-secrets-cache/actions/workflows/release.yml/badge.svg)](https://github.com/rnag/py-secrets-cache/actions/workflows/release.yml)
[![Documentation Status](https://readthedocs.org/projects/secrets-cache/badge/?version=latest)](https://secrets-cache.readthedocs.io/en/latest/?version=latest)

Cache secrets locally from AWS Secrets Manager and other secret stores, with optional local caching for development or Lambda-friendly usage.

* PyPI package: https://pypi.org/project/secrets-cache/
* Free software: MIT License
* Documentation: https://secrets-cache.readthedocs.io.

## Installation

Install the base package (minimal, Lambda-friendly):

```bash
pip install secrets-cache[lambda]
````

For local development or testing (with local TOML caching, AWS SDK):

```bash
pip install secrets-cache[local]
```

Optional CLI tools:

```bash
pip install secrets-cache[cli]
```

## Usage

### Fetch a secret from AWS Secrets Manager

```python
from secrets_cache import get_secret

# Returns JSON-decoded dict if possible
db_creds = get_secret("prod/AppBeta/MySQL")

# Returns raw string
raw_value = get_secret("prod/AppBeta/MySQL", raw=True)

# Force refresh from AWS, ignoring cache
fresh_value = get_secret("prod/AppBeta/MySQL", force_refresh=True)
```

### Fetch a parameter from AWS SSM Parameter Store

```python
from secrets_cache import get_param

api_url = get_param("prod/AppBeta/API_URL")
```

**Notes:**

* Secrets and parameters are **cached in-memory** and optionally in a **local TOML file** (`~/.secrets_cache.toml`) for repeated calls.
* Default cache TTL is **1 week** (configurable via `SECRETS_CACHE_TTL` environment variable).
* AWS region defaults to `AWS_REGION` environment variable or `us-east-1`.
* Module-level caches persist across **warm AWS Lambda invocations**, so repeated calls in the same container are very fast.

## Features

* Fetch secrets and parameters from AWS Secrets Manager / SSM.
* Module-level caching for in-process efficiency.
* Optional TOML caching for development.
* Lambda-friendly usage without extra dependencies.
* Easy to extend to other secret stores in the future.

## Getting Started: AWS Lambda

When running in AWS Lambda, you usually don’t want file-based caching. Use the `lambda` extra:

```bash
pip install secrets-cache[lambda]
````

### Example Lambda handler

```python
import json
from secrets_cache import get_secret, get_param

def lambda_handler(event, context):
    # Get a secret from AWS Secrets Manager
    db_password = get_secret("my-db-password", region="us-east-1")

    # Get a parameter from AWS SSM Parameter Store
    api_key = get_param("/my/api/key", region="us-east-1")

    # Do something with your secrets
    return {
        "statusCode": 200,
        "body": json.dumps({
            "db_password_length": len(db_password),
            "api_key_length": len(api_key)
        })
    }
```

### Notes for Lambda

* **Module-level caching** ensures repeated calls in the same container are very fast.
* No TOML or local file access is required — perfect for ephemeral Lambda environments.
* Secrets are cached **in memory only**, and each new container start fetches them from AWS.
* If you want local development caching, install the `local` extra:

```bash
pip install secrets-cache[local]
```

This enables optional `~/.secrets_cache.toml` caching for local testing.

## Credits

Created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [rnag/cookiecutter-pypackage](https://github.com/rnag/cookiecutter-pypackage) template.
