"""
FFTN_BTC_1D Custom Exceptions
"""


class FFTNError(Exception):
    """
    Base project exception.
    """
    pass


class DataNotFoundError(FFTNError):
    """
    Raised when required data is missing.
    """
    pass