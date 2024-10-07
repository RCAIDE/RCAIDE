# RCAIDE/Framework/Missions/Conditions/Numerics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
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
    control_points: np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    differentiate:  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    integrate:      np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


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

    dimensionless:              NumericalTime   = field(default_factory=lambda: NumericalTime(name='Dimensionless Time'))
    time:                       NumericalTime   = field(default_factory=lambda: NumericalTime(name='Time'))

    def __post_init__(self):
        self.discretization_method = lambda: chebyshev_matrices(n=self.number_of_control_points,
                                                                calculate_integration=self.calculate_integration,
                                                                spacing=self.control_point_spacing)

        (self.dimensionless.control_points,
         self.dimensionless.differentiate,
         self.dimensionless.integrate) = self.discretization_method()

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestNumericalTime(unittest.TestCase):
    def setUp(self):
        self.numerical_time = NumericalTime()

    def test_default_values(self):
        self.assertTrue(np.array_equal(self.numerical_time.control_points, np.zeros((1, 1))))
        self.assertTrue(np.array_equal(self.numerical_time.differentiate, np.zeros((1, 1))))
        self.assertTrue(np.array_equal(self.numerical_time.integrate, np.zeros((1, 1))))


class TestNumerics(unittest.TestCase):
    def setUp(self):
        self.numerics = Numerics()

    def test_default_values(self):
        self.assertEqual(self.numerics.name, 'Numerics')
        self.assertEqual(self.numerics.number_of_control_points, 16)
        self.assertEqual(self.numerics.control_point_spacing, 'cosine')
        self.assertTrue(self.numerics.calculate_integration)
        self.assertIsNone(self.numerics.solver_jacobian)
        self.assertEqual(self.numerics.solution_tolerance, 1e-8)
        self.assertEqual(self.numerics.max_evaluations, int(1e4))
        self.assertIsNone(self.numerics.step_size)
        self.assertFalse(self.numerics.converged)

    def test_dimensionless_and_time_attributes(self):
        self.assertIsInstance(self.numerics.dimensionless, NumericalTime)
        self.assertIsInstance(self.numerics.time, NumericalTime)
        self.assertEqual(self.numerics.dimensionless.name, 'Dimensionless Time')
        self.assertEqual(self.numerics.time.name, 'Time')

    def test_custom_values(self):
        custom_numerics = Numerics(
            name='Custom Numerics',
            number_of_control_points=20,
            control_point_spacing='linear',
            calculate_integration=False,
            solver_jacobian='custom_jacobian',
            solution_tolerance=1e-6,
            max_evaluations=1000,
            step_size=0.1,
            converged=True
        )
        self.assertEqual(custom_numerics.name, 'Custom Numerics')
        self.assertEqual(custom_numerics.number_of_control_points, 20)
        self.assertEqual(custom_numerics.control_point_spacing, 'linear')
        self.assertFalse(custom_numerics.calculate_integration)
        self.assertEqual(custom_numerics.solver_jacobian, 'custom_jacobian')
        self.assertEqual(custom_numerics.solution_tolerance, 1e-6)
        self.assertEqual(custom_numerics.max_evaluations, 1000)
        self.assertEqual(custom_numerics.step_size, 0.1)
        self.assertTrue(custom_numerics.converged)


if __name__ == '__main__':
    unittest.main()

