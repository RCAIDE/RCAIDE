# RCAIDE/Library/Methods/Energy/Converters/flow.py
# (c) Copyright 2025 Aerospace Research Community LLC#
# Created:  May 2025, J. Smart
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# Package Imports

import jax.numpy as np
from scipy.optimize import fsolve


# ----------------------------------------------------------------------------------------------------------------------
#  Sonic Split
# ----------------------------------------------------------------------------------------------------------------------


def sonic_split(
    func,
    M0,
):
    # Initializing the array
    M1_guess = np.ones_like(M0)

    # Separating supersonic and subsonic solutions
    i_low = M0 < 1.0
    i_high = M0 >= 1.0

    # Subsonic solution initialization
    M1_guess[i_low] = 0.1

    # Supersonic solution initialization
    M1_guess[i_high] = 1.1

    # Solving
    M1 = fsolve(func, M1_guess, factor=0.1)

    return M1


def fM(
    AR,
    M0,
    g,
):
    f = lambda M1: ((M0 / M1 *
                     ((1. + (g - 1.) / 2. * M1 ** 2) / (1. + (g - 1.) / 2. * M0 ** 2)) ** ((g + 1.) / (2. * (g - 1.))))
                    - AR)

    M1 = sonic_split(f, M0)

    return M1


def Rayleigh(
    Tt_R,
    M0,
    g,
):
    f = lambda M1: (((1. + g * M0 ** 2) ** 2. * M1 ** 2 * (1. + (g - 1.) / 2. * M1 ** 2)) /
                    ((1. + g * M1 ** 2) ** 2. * M0 ** 2 * (1. + (g - 1.) / 2. * M0 ** 2))
                    - Tt_R)

    M1 = sonic_split(f, M0)

    Pt_R = (
        (1. + g * M0 ** 2) /
        (1. + g * M1 ** 2) * (
            (1. + (g - 1.) / 2. * M1 ** 2) / (1. + (g - 1.) / 2. * M0 ** 2)
        ) ** (g / (g - 1.))
    )

    return M1, Pt_R


