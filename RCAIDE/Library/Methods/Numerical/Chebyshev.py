# RCAIDE/Library/Methods/Numerical/Chebyshev.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from warnings import warn

# package imports
import numpy as np

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Chebyshev Pseudospectral Matrices
# ----------------------------------------------------------------------------------------------------------------------


def chebyshev_matrices(n: int = 16,
                       calculate_integration: bool = True,
                       spacing: str = 'cosine'):

    assert n > 0, "Attempted to calculate Chebyshev matrices with non-positive number of control points."

    if spacing == 'linear':
        x = np.linspace(0, 1, n)
    else:
        x = 0.5 * (1 - np.cos(np.pi * np.arange(n) / (n - 1)))

    if spacing not in ['linear', 'cosine']:
        warn("Invalid control point spacing. Defaulting to cosine spacing.")

    c = np.array([2.] + [1.] * (n - 2) + [2.])
    c *= (-1.) ** np.arange(n)
    c_inv = 1./c

    A = np.tile(x, (n, 1)).T
    dA = A - A.T + np.eye(n)

    cs = np.multiply(np.atleast_2d(c), np.atleast_2d(c_inv).T)
    D = np.divide(cs.T, dA)

    D -= np.diag(np.sum(D.T, axis=0))

    if calculate_integration:
        # Invert D, trimming first row and column
        I = np.linalg.inv(D[1:, 1:])

        # Repack missing columns with zeros
        I = np.append(np.zeros((1, n - 1)), I, axis=0)
        I = np.append(np.zeros((n, 1)), I, axis=1)

        return np.atleast_2d(x), D, I

    else:

        return np.atleast_2d(x), D, None