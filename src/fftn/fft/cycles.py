"""
FFTN_BTC_1D

MODULE: FFT
COMPONENT: Cycle Detection

RESPONSIBILITY:
    Convert frequency components
    into cycle periods.

INPUT:
    Ranked frequency spectrum.

OUTPUT:
    Frequency components converted
    into cycle periods.

DO NOT:
    - Perform FFT
    - Load external data
    - Forecast prices
"""


def extract_cycles(spectrum):
    """
    Convert FFT frequencies into cycle periods.

    Parameters
    ----------
    spectrum : list of dict
        Output from compute_spectrum().

    Returns
    -------
    cycles : list of dict
        Cycle information ranked by spectral power.
    """

    cycles = []

    for component in spectrum:

        frequency = component["frequency"]

        if frequency <= 0:
            continue

        period = 1.0 / frequency

        cycles.append(
            {
                "period": period,
                "frequency": frequency,
                "amplitude": component["amplitude"],
                "power": component["power"],
            }
        )

    return cycles