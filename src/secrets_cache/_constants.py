"""Constants"""
import os


DEFAULT_AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

DEFAULT_CACHE_TTL = int(os.getenv('SECRETS_CACHE_TTL', 7 * 24 * 3600))
