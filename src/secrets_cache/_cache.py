"""Caching module."""
from pathlib import Path
from time import time


# TOML cache file (optional)
_CACHE_FILE = Path.home() / '.secrets_cache.toml'


# Lazy-loaded cache
_cache = None


# Optional: import TOML only if available
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        # noinspection SpellCheckingInspection
        import tomli as tomllib  # Python 3.10
    except ImportError:
        # noinspection SpellCheckingInspection
        tomllib = None

try:
    import tomli_w
except ImportError:
    tomli_w = None


def _load_cache() -> dict:
    global _cache

    if _cache is None:
        if tomllib and _CACHE_FILE.exists():
            with _CACHE_FILE.open('rb') as f:
                _cache = tomllib.load(f)
        else:
            _cache = {}

    return _cache


def _save_cache() -> None:
    if (_cache is None
            or not tomli_w
            or not _CACHE_FILE.parent.exists()):
        return

    with _CACHE_FILE.open('wb') as f:
        tomli_w.dump(_cache, f)  # type: ignore


def get_cached_value(service: str, name: str, now: float, ttl: int):
    data = _load_cache()
    service_cache = data.get(service, {})
    entry = service_cache.get(name)

    if entry and (now - entry['fetched_at'] < ttl):
        return entry['value']

    return None


def update_cache(service: str, name: str, value: str, now: float):
    data = _load_cache()
    final_value = {'value': value, 'fetched_at': now}

    service_cache = data.get(service)

    if service_cache is None:
        data[service] = {name: final_value}
    else:
        service_cache[name] = final_value

    _save_cache()


def cached_fetch(service: str, key: str, region: str, fetcher, ttl: int, force_refresh: bool):
    """Fetch from cache or call fetcher."""
    now = int(time())

    if not force_refresh:
        if (value := get_cached_value(service, key, now, ttl)) is not None:
            return value

    value = fetcher(key, region)
    if value is not None:
        update_cache(service, key, value, now)
    return value
