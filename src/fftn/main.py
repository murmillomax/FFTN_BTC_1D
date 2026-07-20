"""
FFTN_BTC_1D

Bitcoin Daily Forecasting Engine

Main entry point.
"""

from fftn.core import config
from fftn.core.logger import get_logger


def main():

    logger = get_logger()

    logger.info("Starting FFTN_BTC_1D")
    logger.info(f"Version: {config.VERSION}")
    logger.info(f"Symbol: {config.SYMBOL}")
    logger.info(f"Timeframe: {config.TIMEFRAME}")
    logger.info(f"Forecast horizon: {config.FORECAST_DAYS} days")


if __name__ == "__main__":
    main()