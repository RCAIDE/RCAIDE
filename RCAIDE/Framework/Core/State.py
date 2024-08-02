# RCAIDE/Framework/Core/State.py
# (c) Copyright 2024 Aerospace Research Community LC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Chebyshev Pseudospectral Matrices
# ----------------------------------------------------------------------------------------------------------------------


def _chebyshev_matrices(n: int = 16,
                        calculate_integration: bool = True,
                        cosine_spacing: bool = True):

    assert n > 0, "Attempted to calculate Chebyshev matrices with non-positive number of control points."

    if cosine_spacing:
        x = 0.5 * (1 - np.cos(np.pi * np.arange(n) / (n - 1)))
    else:
        x = np.linspace(0, 1, n)

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
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Conditions:

    name: str = 'Conditions'

    number_of_rows: int = 1
    adjustment_from_parent: int = 0
    array: np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))

    def __post_init__(self):
        self.expand_rows(self.number_of_rows)

    def expand_rows(self, rows: int, override: bool = False):

        self.number_of_rows = np.maximum(rows - self.adjustment_from_parent, 0)

        for k, v in vars(self).items():
            if isinstance(v, Conditions):
                v.expand_rows(rows, override=override)
            elif isinstance(v, np.ndarray):
                vars(self)[k] = np.resize(v, (self.number_of_rows, v.shape[1]))

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Time(Conditions):

    control_points: np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))
    differentiate: np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))
    integrate: np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))


@dataclass(kw_only=True)
class Numerics:

    name: str = 'Numerics'

    number_of_control_points: int = 16
    discretization_method: str = 'cosine'

    solver_jacobian: str = None
    solution_tolerance: float = 1e-8
    max_evaluations: int = 0

    step_size: float = None
    converged: bool = False

    dimensionless = Time(name='Dimensionless Time')
    time = Time(name='Time')

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class State(Conditions):

    name: str = 'State'

    conditions: Conditions = Conditions()
    numerics: Numerics = Numerics()

    initials:   np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))
    unknowns:   np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))
    residuals:  np.ndarray = field(init=False, default_factory=lambda: np.ndarray((0, 0)))


if __name__ == '__main__':
    cond = Conditions()
    print(cond)
