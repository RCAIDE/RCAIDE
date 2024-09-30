# RCAIDE/Framework/Missions/Conditions/AeroDerivatives.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
import unittest

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions


# ----------------------------------------------------------------------------------------------------------------------
#  AeroDerivatives
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class CoefficientDerivatives(Conditions):
    """
    A class representing coefficient derivatives in aerodynamic conditions.

    This class stores various flight parameters that are used to calculate
    aerodynamic coefficient derivatives.

    Attributes
    ----------
    name : str
        The name of the coefficient derivatives set. Default is 'Coefficient Derivatives'.
    alpha : np.ndarray
        The derivative w.r.t. angle of attack, stored as a 1x1 numpy array. Default is zeros((1, 1)).
    beta : np.ndarray
        The derivative w.r.t. sideslip angle, stored as a 1x1 numpy array. Default is zeros((1, 1)).
    v : np.ndarray
        The derivative w.r.t.velocity, stored as a 1x1 numpy array. Default is zeros((1, 1)).
    throttle : np.ndarray
        The derivative w.r.t. throttle setting, stored as a 1x1 numpy array. Default is zeros((1, 1)).

    Notes
    -----
    All attributes are initialized as 1x1 numpy arrays, allowing for easy expansion
    to store multiple values if needed.
    """

    # Attribute     Type        Default Value
    name: str = 'Coefficient Derivatives'

    alpha: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    beta: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    v: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    throttle: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class AeroDerivativesConditions(Conditions):
    """
    A class representing aerodynamic derivative conditions.

    This class stores coefficient derivatives for lift and drag,
    which are essential for analyzing the aerodynamic behavior of an aircraft.

    Attributes
    ----------
    name : str
        The name of the aerodynamic derivatives set. Default is 'Aerodynamic Derivatives'.
    dCL : CoefficientDerivatives
        The lift coefficient derivatives, including derivatives with respect to
        angle of attack, sideslip angle, velocity, and throttle.
    dCD : CoefficientDerivatives
        The drag coefficient derivatives, including derivatives with respect to
        angle of attack, sideslip angle, velocity, and throttle.

    Notes
    -----
    This class inherits from the Conditions base class and uses the dataclass
    decorator with keyword-only arguments.
    """

    # Attribute      Type        Default Value
    name: str = 'Aerodynamic Derivatives'

    dCL: CoefficientDerivatives = field(default_factory=lambda:
    CoefficientDerivatives(name='Lift Coefficient Derivatives'))
    dCD: CoefficientDerivatives = field(default_factory=lambda:
    CoefficientDerivatives(name='Drag Coefficient Derivatives'))


class TestCoefficientDerivatives(unittest.TestCase):
    def setUp(self):
        self.coeff_derivatives = CoefficientDerivatives()

    def test_default_name(self):
        self.assertEqual(self.coeff_derivatives.name, 'Coefficient Derivatives')

    def test_custom_name(self):
        custom_coeff = CoefficientDerivatives(name='Custom Coefficients')
        self.assertEqual(custom_coeff.name, 'Custom Coefficients')

    def test_default_array_shapes(self):
        attrs = ['alpha', 'beta', 'v', 'throttle']
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(self.coeff_derivatives, attr).shape, (1, 1))

    def test_array_mutability(self):
        self.coeff_derivatives.alpha[0, 0] = 1.0
        self.assertEqual(self.coeff_derivatives.alpha[0, 0], 1.0)

    def test_array_expansion(self):
        self.coeff_derivatives.v = np.zeros((3, 3))
        self.assertEqual(self.coeff_derivatives.v.shape, (3, 3))


class TestAeroDerivativesConditions(unittest.TestCase):
    def setUp(self):
        self.aero_derivatives = AeroDerivativesConditions()

    def test_default_name(self):
        self.assertEqual(self.aero_derivatives.name, 'Aerodynamic Derivatives')

    def test_custom_name(self):
        custom_aero = AeroDerivativesConditions(name='Custom Aero')
        self.assertEqual(custom_aero.name, 'Custom Aero')

    def test_dCL_instance(self):
        self.assertIsInstance(self.aero_derivatives.dCL, CoefficientDerivatives)
        self.assertEqual(self.aero_derivatives.dCL.name, 'Lift Coefficient Derivatives')

    def test_dCD_instance(self):
        self.assertIsInstance(self.aero_derivatives.dCD, CoefficientDerivatives)
        self.assertEqual(self.aero_derivatives.dCD.name, 'Drag Coefficient Derivatives')

    def test_dCL_attributes(self):
        attrs = ['alpha', 'beta', 'v', 'throttle']
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(self.aero_derivatives.dCL, attr).shape, (1, 1))

    def test_dCD_attributes(self):
        attrs = ['alpha', 'beta', 'v', 'throttle']
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(self.aero_derivatives.dCD, attr).shape, (1, 1))

    def test_dCL_mutability(self):
        self.aero_derivatives.dCL.alpha[0, 0] = 1.0
        self.assertEqual(self.aero_derivatives.dCL.alpha[0, 0], 1.0)

    def test_dCD_mutability(self):
        self.aero_derivatives.dCD.beta[0, 0] = 2.0
        self.assertEqual(self.aero_derivatives.dCD.beta[0, 0], 2.0)


if __name__ == '__main__':
    unittest.main()