"""
FFTN_BTC_1D

MODULE: FFT
COMPONENT: Transform

RESPONSIBILITY:
    Apply Fast Fourier Transform (FFT)
    to time series data.

INPUT:
    Time series signal.

OUTPUT:
    Frequencies
    Amplitudes
    Phases

DO NOT:
    - Forecast prices
    - Load external data
    - Validate models
"""


import numpy as np


def compute_fft(signal):
    """
    Compute Fast Fourier Transform.

    Parameters
    ----------
    signal : array-like
        Time series values.

    Returns
    -------
    frequencies : ndarray
        Frequency components.

    amplitudes : ndarray
        Magnitude of each frequency.

    phases : ndarray
        Phase angle of each frequency.
    """

    signal = np.asarray(signal)

    n = len(signal)

    # FFT
    fft_values = np.fft.fft(signal)

    # Frequencies
    frequencies = np.fft.fftfreq(n)

    # Amplitude
    amplitudes = np.abs(fft_values)

    # Phase
    phases = np.angle(fft_values)

    return frequencies, amplitudes, phases