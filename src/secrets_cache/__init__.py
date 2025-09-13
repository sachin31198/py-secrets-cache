"""Secrets Cache Library - get AWS secrets and SSM parameters with optional caching."""
from ._aws import get_secret, get_param

__all__ = ["get_secret", "get_param"]

__author__ = """Ritvik Nag"""
__email__ = 'me@ritviknag.com'
