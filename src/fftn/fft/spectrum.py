"""
FFTN_BTC_1D

MODULE: FFT
COMPONENT: Spectrum Analysis

RESPONSIBILITY:
    Analyze FFT output and calculate
    spectral power.

INPUT:
    Frequencies
    Amplitudes

OUTPUT:
    Ranked frequency components

DO NOT:
    - Load external data
    - Perform FFT
    - Forecast prices
"""


import numpy as np


def compute_spectrum(frequencies, amplitudes):
    """
    Calculate spectral power and rank frequencies.

    Parameters
    ----------
    frequencies : array-like
        FFT frequency components.

    amplitudes : array-like
        FFT amplitudes.

    Returns
    -------
    spectrum : list of dict
        Ranked frequency components.
    """

    frequencies = np.asarray(frequencies)
    amplitudes = np.asarray(amplitudes)

    # Remove zero frequency (DC component)
    mask = frequencies != 0

    frequencies = frequencies[mask]
    amplitudes = amplitudes[mask]

    # Keep only positive frequencies
    mask = frequencies > 0

    frequencies = frequencies[mask]
    amplitudes = amplitudes[mask]

    # Power spectrum
    power = amplitudes ** 2

    # Sort by power descending
    order = np.argsort(power)[::-1]

    spectrum = []

    for i in order:
        spectrum.append(
            {
                "frequency": frequencies[i],
                "amplitude": amplitudes[i],
                "power": power[i],
            }
        )

    return spectrum