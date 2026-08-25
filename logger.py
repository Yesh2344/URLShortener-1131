"""
Centralised logger configuration.
"""

import logging
import sys
from config import settings

def get_logger(name: str = "urlshortener") -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        # Logger already configured
        return logger

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.propagate = False
    return logger

# Export a module‑level logger
log = get_logger()