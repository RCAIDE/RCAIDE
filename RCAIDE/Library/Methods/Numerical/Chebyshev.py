# RCAIDE/Library/Methods/Numerical/Chebyshev.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
from typing import Callable

# package imports
import numpy as np

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Chebyshev Pseudospectral Matrices
# ----------------------------------------------------------------------------------------------------------------------




def chebyshev_matrices(n: int = 16,
                       spacing_function: Callable = lambda n: 0.5 * (1 - np.cos(np.pi * np.arange(n) / (n - 1)))
                       ):
    """
    Calculate Chebyshev pseudospectral matrices for numerical differentiation and integration.

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

    c = np.array([2.] + [1.] * (n - 2) + [2.])
    c *= (-1.) ** np.arange(n)
    c_inv = 1./c

    A = np.tile(x, (n, 1)).T
    dA = A - A.T + np.eye(n)

    cs = np.multiply(np.atleast_2d(c), np.atleast_2d(c_inv).T)
    D = np.divide(cs.T, dA)

    D -= np.diag(np.sum(D.T, axis=0))

    # Invert D, trimming first row and column
    I = np.linalg.inv(D[1:, 1:])

    # Repack missing columns with zeros
    I = np.append(np.zeros((1, n - 1)), I, axis=0)
    I = np.append(np.zeros((n, 1)), I, axis=1)

    return np.atleast_2d(x), D, I

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestChebyshevMatrices(unittest.TestCase):

    def test_default_parameters(self):
        x, D, I = chebyshev_matrices()
        self.assertEqual(x.shape, (1, 16))
        self.assertEqual(D.shape, (16, 16))
        self.assertEqual(I.shape, (16, 16))

    def test_custom_n(self):
        x, D, I = chebyshev_matrices(n=10)
        self.assertEqual(x.shape, (1, 10))
        self.assertEqual(D.shape, (10, 10))
        self.assertEqual(I.shape, (10, 10))

    def test_default_spacing(self):
        x, _, _ = chebyshev_matrices()
        expected_x = 0.5 * (1 - np.cos(np.pi * np.arange(16) / 15))
        self.assertTrue(np.allclose(x, expected_x.reshape(1, -1)))

    def test_custom_spacing_function(self):
        linear_spacing = lambda n: np.linspace(0, 1, n)
        x, _, _ = chebyshev_matrices(n=16, spacing_function=linear_spacing)
        self.assertTrue(np.allclose(x, np.linspace(0, 1, 16).reshape(1, -1)))

    def test_negative_n(self):
        with self.assertRaises(AssertionError):
            chebyshev_matrices(n=-1)

    def test_zero_n(self):
        with self.assertRaises(AssertionError):
            chebyshev_matrices(n=0)

    def test_differentiation_matrix_properties(self):
        _, D, _ = chebyshev_matrices()
        self.assertTrue(np.allclose(np.sum(D, axis=1), 0))  # Row sum should be zero

    def test_integration_matrix_properties(self):
        _, D, I = chebyshev_matrices()
        self.assertTrue(np.allclose(np.dot(D[1:, 1:], I[1:, 1:]), np.eye(15)))  # DI should be identity (except first row/col)

    def test_matrix_shapes(self):
        for n in [5, 10, 20]:
            x, D, I = chebyshev_matrices(n=n)
            self.assertEqual(x.shape, (1, n))
            self.assertEqual(D.shape, (n, n))
            self.assertEqual(I.shape, (n, n))

    def test_spacing_function_output(self):
        def custom_spacing(n):
            return np.sqrt(np.linspace(0, 1, n))

        x, _, _ = chebyshev_matrices(n=16, spacing_function=custom_spacing)
        expected_x = np.sqrt(np.linspace(0, 1, 16))
        self.assertTrue(np.allclose(x, expected_x.reshape(1, -1)))


if __name__ == '__main__':
    unittest.main()
