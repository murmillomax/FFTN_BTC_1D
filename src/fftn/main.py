"""
FFTN_BTC_1D

Bitcoin Daily Forecasting Engine

Main entry point.
"""

# ============================================================
# MODULE: CORE
# PATH: src/fftn/core
# ============================================================

from fftn.core import config
from fftn.core.logger import get_logger


# ============================================================
# MODULE: DATA
# PATH: src/fftn/data
# ============================================================

from fftn.data import get_data_paths, load_data, validate_data

def main():
    
    # ========================================================
    # CORE INITIALIZATION
    # ========================================================

    logger = get_logger()

    logger.info("Starting FFTN_BTC_1D")
    logger.info(f"Version: {config.VERSION}")
    logger.info(f"Symbol: {config.SYMBOL}")
    logger.info(f"Timeframe: {config.TIMEFRAME}")
    logger.info(f"Forecast horizon: {config.FORECAST_DAYS} days")


    # ========================================================
    # DATA INITIALIZATION
    # ========================================================

    paths = get_data_paths()

    logger.info(f"Raw data path: {paths['raw']}")
    logger.info(f"Processed data path: {paths['processed']}")

    load_data()

    validate_data()


if __name__ == "__main__":
    main()