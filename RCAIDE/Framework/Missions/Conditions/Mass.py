# RCAIDE/Framework/Missions/Conditions/Mass.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Mass
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MassConditions(Conditions):
    """
    Represents the mass conditions for a vehicle or system.

    This class extends the Conditions base class to specifically handle mass-related
    parameters and calculations.

    Attributes
    ----------
    name : str
        The name of the mass conditions.

    total : np.ndarray
        The total mass of the system.
    rate_of_change : np.ndarray
        The rate of change of mass.

    total_moment_of_inertia : np.ndarray
        The total moment of inertia.

    breakdown : Conditions
        A nested Conditions object representing the breakdown of mass components.

    Notes
    -----
    All attributes are initialized using default factories to ensure each instance
    has its own copy of mutable objects.
    """

    # Attribute             Type    Default Value
    name:                   str         = 'Mass Conditions'

    total:                  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    rate_of_change:         np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    center_of_gravity:      np.ndarray  = field(default_factory=lambda: np.zeros((1, 1, 3)))
    moments_of_inertia:     np.ndarray  = field(default_factory=lambda: np.zeros((1, 1, 3, 3)))

    breakdown:              Conditions  = field(default_factory=lambda: Conditions(name='Mass Breakdown'))

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestMassConditions(unittest.TestCase):

    def setUp(self):
        self.mass_conditions = MassConditions()

    def test_default_values(self):
        self.assertEqual(self.mass_conditions.name, 'Mass Conditions')
        np.testing.assert_array_equal(self.mass_conditions.total, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.mass_conditions.rate_of_change, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.mass_conditions.total_moment_of_inertia, np.zeros((1, 1, 3)))
        self.assertIsInstance(self.mass_conditions.breakdown, Conditions)
        self.assertEqual(self.mass_conditions.breakdown.name, 'Mass Breakdown')

    def test_custom_name(self):
        custom_mass = MassConditions(name="Custom Mass Conditions")
        self.assertEqual(custom_mass.name, "Custom Mass Conditions")

    def test_total_mass(self):
        self.mass_conditions.total = np.array([[1000.0]])
        np.testing.assert_array_equal(self.mass_conditions.total, np.array([[1000.0]]))

    def test_rate_of_change(self):
        self.mass_conditions.rate_of_change = -0.5
        np.testing.assert_array_equal(self.mass_conditions.rate_of_change, np.array([[-0.5]]))

    def test_total_moment_of_inertia(self):
        moment = np.array([[100.0, 200.0, 300.0]])
        self.mass_conditions.total_moment_of_inertia = moment
        np.testing.assert_array_equal(self.mass_conditions.total_moment_of_inertia, moment)

    def test_breakdown(self):
        self.mass_conditions.breakdown.fuel = np.array([[500.0]])
        self.mass_conditions.breakdown.payload = np.array([[200.0]])
        np.testing.assert_array_equal(self.mass_conditions.breakdown.fuel, np.array([[500.0]]))
        np.testing.assert_array_equal(self.mass_conditions.breakdown.payload, np.array([[200.0]]))

    def test_array_shapes(self):
        self.assertEqual(self.mass_conditions.total.shape, (1, 1))
        self.assertEqual(self.mass_conditions.rate_of_change.shape, (1, 1))
        self.assertEqual(self.mass_conditions.total_moment_of_inertia.shape, (1, 1, 3))


if __name__ == '__main__':
    unittest.main()
