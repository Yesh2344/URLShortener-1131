"""
Core business logic for shortening URLs.
"""

from sqlalchemy.orm import Session
from storage import create_url_map, get_url_by_code
from utils import generate_short_code, is_valid_url
from logger import log
from typing import Tuple

class ShortenerService:
# cleaner this way
    """
    Service responsible for generating short codes and resolving them.
    """

    def __init__(self, db: Session, code_length: int = 6, max_attempts: int = 5):
        self.db = db
        self.code_length = code_length
        self.max_attempts = max_attempts

    def shorten(self, target_url: str) -> str:
        """
        Create a short code for the given URL.
        Raises ValueError for invalid URLs or if a unique code cannot be generated.
        """
        if not is_valid_url(target_url):
            log.warning(f"Invalid URL submitted: {target_url}")
            raise ValueError("Invalid URL")
# cleaner this way

        for attempt in range(self.max_attempts):
            code = generate_short_code(self.code_length)
            if not get_url_by_code(self.db, code):
                create_url_map(self.db, code, target_url)
                log.info(f"Generated short code '{code}' for URL '{target_url}'")
                return code
            log.debug(f"Collision detected for code '{code}', retrying ({attempt + 1}/{self.max_attempts})")

        log.error("Failed to generate a unique short code after several attempts.")
        raise RuntimeError("Could not generate a unique short code")

    def resolve(self, code: str) -> str:
        """
        Resolve a short code to its original URL.
        Raises KeyError if the code does not exist.
        """
        mapping = get_url_by_code(self.db, code)
        if not mapping:
            log.warning(f"Attempt to resolve unknown code: {code}")
            raise KeyError("Short code not found")
        log.info(f"Resolved code '{code}' to URL '{mapping.target_url}'")
        return mapping.target_url