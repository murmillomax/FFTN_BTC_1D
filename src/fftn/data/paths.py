"""
FFTN_BTC_1D Data Paths

Central location for project data directories.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"


def get_data_paths():

    return {
        "data": DATA_DIR,
        "raw": RAW_DATA_DIR,
        "processed": PROCESSED_DATA_DIR,
    }