"""
FFTN_BTC_1D

TEST: FFT Pipeline

Flow:
    Signal
      |
      v
    FFT
      |
      v
    Spectrum
      |
      v
    Cycles
"""


import numpy as np

from fftn.fft.transform import compute_fft
from fftn.fft.spectrum import compute_spectrum
from fftn.fft.cycles import extract_cycles


def test_fft_pipeline():

    # Synthetic signal
    # Expected period = 10 samples

    n = 100

    x = np.arange(n)

    signal = np.sin(2 * np.pi * x / 10)


    # FFT

    frequencies, amplitudes, phases = compute_fft(signal)


    # Spectrum

    spectrum = compute_spectrum(
        frequencies,
        amplitudes
    )


    # Cycles

    cycles = extract_cycles(spectrum)


    dominant_period = cycles[0]["period"]


    print("\nDominant period:")
    print(dominant_period)


    assert abs(dominant_period - 10) < 0.1