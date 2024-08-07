# RCAIDE/Framework/Missions/Conditions/Numerics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from warnings import warn
from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Chebyshev Pseudospectral Matrices
# ----------------------------------------------------------------------------------------------------------------------


def _chebyshev_matrices(n: int = 16,
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

        return x, D, I

    else:

        return x, D, None

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class NumericalTime(Conditions):

    #Attribute      Type        Default Value
    control_points: np.ndarray  = field(default_factory=lambda: np.ndarray((0, 0)))
    differentiate:  np.ndarray  = field(default_factory=lambda: np.ndarray((0, 0)))
    integrate:      np.ndarray  = field(default_factory=lambda: np.ndarray((0, 0)))


@dataclass(kw_only=True)
class Numerics(Conditions):

    # Attribute                 Type            Default Value
    name:                       str             = 'Numerics'

    number_of_control_points:   int             = 16
    control_point_spacing:      str             = 'cosine'
    calculate_integration:      bool            = True
    discretization_method:      Callable        = None

    solver_jacobian:            str             = None
    solution_tolerance:         float           = 1e-8
    max_evaluations:            int             = int(1e4)

    step_size:                  float           = None
    converged:                  bool            = False

    dimensionless:              NumericalTime   = NumericalTime(name='Dimensionless Time')
    time:                       NumericalTime   = NumericalTime(name='Time')

    def __post_init__(self):
        self.discretization_method = lambda: _chebyshev_matrices(n=self.number_of_control_points,
                                                                 calculate_integration=self.calculate_integration,
                                                                 spacing=self.control_point_spacing)

