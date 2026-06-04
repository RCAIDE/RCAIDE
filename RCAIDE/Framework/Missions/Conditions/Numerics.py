# RCAIDE/Framework/Missions/Conditions/Numerics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------


def chebyshev_matrices(n: int = 16,
                       calculate_integration: bool = True,
                       ):

    assert n > 0, "Attempted to calculate Chebyshev matrices with non-positive number of control points."

    x = 0.5 * (1 - jnp.cos(jnp.pi * jnp.arange(n) / (n - 1)))

    c = jnp.array([2.] + [1.] * (n - 2) + [2.])
    c *= (-1.) ** jnp.arange(n)
    c_inv = 1./c

    A = jnp.tile(x, (n, 1)).T
    dA = A - A.T + jnp.eye(n)

    cs = jnp.multiply(jnp.atleast_2d(c), jnp.atleast_2d(c_inv).T)
    D = jnp.divide(cs.T, dA)

    D -= jnp.diag(jnp.sum(D.T, axis=0))

    if calculate_integration:
        # Invert D, trimming first row and column
        I = jnp.linalg.inv(D[1:, 1:])

        # Repack missing columns with zeros
        I = jnp.append(jnp.zeros((1, n - 1)), I, axis=0)
        I = jnp.append(jnp.zeros((n, 1)), I, axis=1)
    else:
        I = None

    return jnp.atleast_2d(x).T, D, I


class NumericalTime(Conditions):

    # Attribute     Type                Default Value
    control_points: jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    differentiate:  jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    integrate:      jnp.ndarray | None  = None

    def __repr__(self):
        return ""


class Numerics(Conditions):

    # Attribute                 Type                Default Value
    tag:                        str                 = eqx.field(static=True, default='Numerics')

    number_of_control_points:   int                 = eqx.field(static=True, default=16)
    control_point_spacing:      str                 = eqx.field(static=True, default='cosine')
    calculate_integration:      bool                = eqx.field(static=True, default=True)
    discretization_method:      Callable | None     = eqx.field(static=True, default=None)

    solver_jacobian:            str | None          = eqx.field(static=True, default=None)
    solution_tolerance:         float               = eqx.field(static=True, default=1e-8)
    max_evaluations:            int                 = eqx.field(static=True, default=int(500))
    step_size:                  float | None        = eqx.field(static=True, default=None)
    
    converged:                  bool                = False

    dimensionless:              NumericalTime   = eqx.field(default_factory=lambda: NumericalTime(tag='Dimensionless Time'))
    time:                       NumericalTime   = eqx.field(default_factory=lambda: NumericalTime(tag='Time'))

    def __post_init__(self):
        # Guard against abstract tracers during JIT
        if self.number_of_control_points <= 1:
            return

        # Calculate the matrices (finite-difference psudospectral operators)
        if self.discretization_method:
            cps, diff, intg = self.discretization_method()
        else:
            cps, diff, intg = chebyshev_matrices(
                 n=self.number_of_control_points,
                 calculate_integration=self.calculate_integration
            )

        new_dimensionless = NumericalTime(
            tag='Dimensionless Time',
            control_points=cps,
            differentiate=diff,
            integrate=intg
        )

        object.__setattr__(self, "dimensionless", new_dimensionless)