"""
FFTN_BTC_1D Logging System
"""

import logging


def get_logger(name="FFTN_BTC_1D"):

    logger = logging.getLogger(name)

    if not logger.handlers:

        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.setLevel(logging.INFO)

    return logger