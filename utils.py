"""
Utility functions used across the project.
"""

import string
import random
from urllib.parse import urlparse
from typing import Optional

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric short code.
    :param length: Length of the code.
    :return: Random string.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url: str) -> bool:
    """
    Very light URL validation.
    :param url: URL to validate.
    :return: True if URL has a scheme and netloc.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False