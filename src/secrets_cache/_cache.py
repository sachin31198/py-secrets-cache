from time import time


def cached_fetch(cache: dict, key: str, region: str, fetcher, ttl: int):
    """Fetch from cache or call fetcher."""
    now = time()
    entry = cache.get(key)
    if entry and (now - entry['fetched_at'] < ttl):
        return entry['value']

    value = fetcher(key, region)
    cache[key] = {'value': value, 'fetched_at': now}
    return value
