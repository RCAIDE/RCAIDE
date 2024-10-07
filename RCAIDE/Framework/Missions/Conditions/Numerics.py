# RCAIDE/Framework/Missions/Conditions/Numerics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable
from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions
from RCAIDE.Library.Methods.Numerical import chebyshev_matrices

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class NumericalTime(Conditions):

    # Attribute     Type        Default Value
    control_points: np.ndarray  = field(default_factory=lambda: np.zeros((0, 0)))
    differentiate:  np.ndarray  = field(default_factory=lambda: np.zeros((0, 0)))
    integrate:      np.ndarray  = field(default_factory=lambda: np.zeros((0, 0)))


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
        self.discretization_method = lambda: chebyshev_matrices(n=self.number_of_control_points,
                                                                calculate_integration=self.calculate_integration,
                                                                spacing=self.control_point_spacing)

        (self.dimensionless.control_points,
         self.dimensionless.differentiate,
         self.dimensionless.integrate) = self.discretization_method()

