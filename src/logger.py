"""
Logging configuration.
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger.

    Args:
        name:
            Logger name.

    Returns:
        Configured logger.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    return logging.getLogger(name)
