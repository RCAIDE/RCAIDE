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
class AeroDerivativesConditions(Conditions):
    """
    A class representing aerodynamic derivative conditions.

    This class stores various aerodynamic derivatives, including the rate of change
    of lift and drag coefficients with respect to different flight parameters.

    Attributes
    ----------
    name : str
        The name of the condition set. Default is 'Aerodynamic Derivatives'.
    dCL_dAlpha : np.ndarray
        The rate of change of lift coefficient with angle of attack.
    dCL_dBeta : np.ndarray
        The rate of change of lift coefficient with sideslip angle.
    dCL_dV : np.ndarray
        The rate of change of lift coefficient with velocity.
    dCL_dThrottle : np.ndarray
        The rate of change of lift coefficient with throttle setting.

    dCD_dAlpha : np.ndarray
        The rate of change of drag coefficient with angle of attack.
    dCD_dBeta : np.ndarray
        The rate of change of drag coefficient with sideslip angle.
    dCD_dV : np.ndarray
        The rate of change of drag coefficient with velocity.
    dCD_dThrottle : np.ndarray
        The rate of change of drag coefficient with throttle setting.

    Notes
    -----
    Each attribute is initialized as a 1x1 numpy array, allowing for easy expansion
    to store multiple values if needed.
    """

    #Attribute      Type        Default Value
    name:           str         = 'Aerodynamic Derivatives'

    # Lift Derivatives

    dCL_dAlpha:     np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCL_dBeta:      np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCL_dV:         np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCL_dThrottle:  np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))

    # Drag Derivatives

    dCD_dAlpha:     np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCD_dBeta:      np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCD_dV:         np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    dCD_dThrottle:  np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))


class TestAeroDerivativesConditions(unittest.TestCase):
    def setUp(self):
        self.aero_derivatives = AeroDerivativesConditions()

    def test_default_name(self):
        self.assertEqual(self.aero_derivatives.name, 'Aerodynamic Derivatives')

    def test_custom_name(self):
        custom_aero = AeroDerivativesConditions(name='Custom Aero')
        self.assertEqual(custom_aero.name, 'Custom Aero')

    def test_default_array_shapes(self):
        attrs = ['dCL_dAlpha', 'dCL_dBeta', 'dCL_dV', 'dCL_dThrottle',
                 'dCD_dAlpha', 'dCD_dBeta', 'dCD_dV', 'dCD_dThrottle']
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(self.aero_derivatives, attr).shape, (1, 1))

    def test_array_mutability(self):
        self.aero_derivatives.dCL_dAlpha[0, 0] = 1.0
        self.assertEqual(self.aero_derivatives.dCL_dAlpha[0, 0], 1.0)

    def test_array_expansion(self):
        self.aero_derivatives.dCD_dV = np.zeros((3, 3))
        self.assertEqual(self.aero_derivatives.dCD_dV.shape, (3, 3))


if __name__ == '__main__':
    unittest.main()