"""Constants"""
import os


DEFAULT_CACHE_TTL = int(os.getenv('SECRETS_CACHE_TTL', 7 * 24 * 3600))
