# RCAIDE/Framework/Missions/Conditions/Numerics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
from typing import Callable
import chex
from dataclasses import field

# package imports
import RNUMPY as rp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Numerics
# ----------------------------------------------------------------------------------------------------------------------


def chebyshev_matrices(n: int = 16,
                       calculate_integration: bool = True,
                       spacing_function: Callable = lambda n: 0.5 * (1 - rp.cos(rp.pi * rp.arange(n) / (n - 1)))
                       ):
    """
    Calculate Chebyshev spectral matrices for numerical differentiation and integration.

    This function computes the Chebyshev collocation points and the corresponding
    differentiation and integration matrices used in spectral methods.

    Parameters:
    -----------
    n : int, optional
        Number of collocation points (default is 16).
    spacing_function : Callable, optional
        A function that takes an integer n and returns an array of n points
        between 0 and 1. By default, it uses a cosine spacing function.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - x : numpy.ndarray
            A 2D array of shape (1, n) containing the collocation points.
        - D : numpy.ndarray
            The differentiation matrix of shape (n, n).
        - I : numpy.ndarray
            The integration matrix of shape (n, n).

    Raises:
    -------
    AssertionError
        If n is not a positive integer.

    Notes:
    ------
    The function uses the Chebyshev differentiation matrix formula and its inverse
    for integration. The first row and column of the integration matrix are set to zero
    to handle the arbitrary constant of integration.
    """

    assert n > 0, "Attempted to calculate Chebyshev matrices with non-positive number of control points."

    x = spacing_function(n)

    c = rp.array([2.] + [1.] * (n - 2) + [2.])
    c *= (-1.) ** rp.arange(n)
    c_inv = 1./c

    A = rp.tile(x, (n, 1)).T
    dA = A - A.T + rp.eye(n)

    cs = rp.multiply(rp.atleast_2d(c), rp.atleast_2d(c_inv).T)
    D = rp.divide(cs.T, dA)

    D -= rp.diag(rp.sum(D.T, axis=0))

    if calculate_integration:
        # Invert D, trimming first row and column
        I = rp.linalg.inv(D[1:, 1:])

        # Repack missing columns with zeros
        I = rp.append(rp.zeros((1, n - 1)), I, axis=0)
        I = rp.append(rp.zeros((n, 1)), I, axis=1)
    else:
        I = None

    return rp.atleast_2d(x).T, D, I


@chex.dataclass(kw_only=True)
class NumericalTime(Conditions):
    """
    A class representing numerical time conditions.

    This class extends the Conditions class and provides attributes for
    control points, differentiation, and integration arrays.

    Attributes
    ----------
    control_points : rp.ndarray
        Array of control points for numerical time calculations.
        Default is a 1x1 array of zeros.
    differentiate : rp.ndarray
        Array for differentiation operations in numerical time calculations.
        Default is a 1x1 array of zeros.
    integrate : rp.ndarray
        Array for integration operations in numerical time calculations.
        Default is a 1x1 array of zeros.

    Notes
    -----
    All attributes are initialized as 1x1 numpy arrays of zeros by default.
    The class uses kw_only=True, meaning all attributes must be specified as
    keyword arguments when instantiating the class.
    """

    # Attribute     Type        Default Value
    control_points: rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    differentiate:  rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    integrate:      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class Numerics(Conditions):

    """
    A class representing numerical conditions for solving differential equations.

    This class extends the Conditions class and provides attributes for
    configuring and storing numerical solution parameters and results.

    Attributes
    ----------
    name : str
        The name of the numerical condition. Default is 'Numerics'.
    number_of_control_points : int
        The number of control points used in the discretization. Default is 16.
    control_point_spacing : str
        The spacing method for control points. Default is 'cosine'.
    calculate_integration : bool
        Flag to determine if integration should be calculated. Default is True.
    discretization_method : Callable
        The method used for discretization. Default is None.
    solver_jacobian : str
        The type of Jacobian used by the solver. Default is None.
    solution_tolerance : float
        The tolerance for the solution convergence. Default is 1e-8.
    max_evaluations : int
        The maximum number of evaluations allowed. Default is 10000.
    step_size : float
        The step size for the numerical method. Default is None.
    converged : bool
        Flag indicating whether the solution has converged. Default is False.
    dimensionless : NumericalTime
        NumericalTime object for dimensionless time calculations.
    time : NumericalTime
        NumericalTime object for time-based calculations.

    Methods
    -------
    __post_init__()
        Initializes the discretization method and computes control points,
        differentiation, and integration matrices.
    """

    # Attribute                 Type            Default Value
    tag:                        str             = 'Numerics'

    number_of_control_points:   int             = 16
    control_point_spacing:      str             = 'cosine'
    calculate_integration:      bool            = True
    discretization_method:      Callable        = None

    solver_jacobian:            str             = None
    solution_tolerance:         float           = 1e-8
    max_evaluations:            int             = int(1e4)

    step_size:                  float           = None
    converged:                  bool            = False

    dimensionless:              NumericalTime   = field(default_factory=lambda: NumericalTime(tag='Dimensionless Time'))
    time:                       NumericalTime   = field(default_factory=lambda: NumericalTime(tag='Time'))

    def __post_init__(self):

        """
        Post-initialization method to set up the discretization method and compute matrices.

        This method is automatically called after the object is initialized. It defaults
        the discretization_method to use Chebyshev PS matrices if no other method is specified
        and computes the control points, differentiation, and integration matrices for dimensionless time.

        Returns
        -------
        None
        """
        if not self.discretization_method:
            self.discretization_method = lambda: chebyshev_matrices(n=self.number_of_control_points,
                                                                    calculate_integration=self.calculate_integration)

        (self.dimensionless.control_points,
         self.dimensionless.differentiate,
         self.dimensionless.integrate) = self.discretization_method()

        super(Numerics, self).__post_init__()

    def expand_rows(self, rows):
        pass  # Avoid resizing control points and differentiation arrays

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestNumericalTime(unittest.TestCase):
    def setUp(self):
        self.numerical_time = NumericalTime()

    def test_default_values(self):
        self.assertTrue(rp.array_equal(self.numerical_time.control_points, rp.zeros((1, 1))))
        self.assertTrue(rp.array_equal(self.numerical_time.differentiate, rp.zeros((1, 1))))
        self.assertTrue(rp.array_equal(self.numerical_time.integrate, rp.zeros((1, 1))))


class TestNumerics(unittest.TestCase):
    def setUp(self):
        self.numerics = Numerics()

    def test_default_values(self):
        self.assertEqual(self.numerics.tag, 'Numerics')
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
        self.assertEqual(self.numerics.dimensionless.tag, 'Dimensionless Time')
        self.assertEqual(self.numerics.time.tag, 'Time')

    def test_custom_values(self):
        custom_numerics = Numerics(
            tag='Custom Numerics',
            number_of_control_points=20,
            control_point_spacing='linear',
            calculate_integration=False,
            solver_jacobian='custom_jacobian',
            solution_tolerance=1e-6,
            max_evaluations=1000,
            step_size=0.1,
            converged=True
        )
        self.assertEqual(custom_numerics.tag, 'Custom Numerics')
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

