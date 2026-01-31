# RCAIDE/Framework/Missions/Conditions/Mass.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
import chex
from dataclasses import field

# package imports
import RNUMPY as rp
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Mass
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class MassConditions(Conditions):
    """
    Represents the mass conditions for a vehicle or system.

    This class extends the Conditions base class to specifically handle mass-related
    parameters and calculations.

    Attributes
    ----------
    name : str
        The name of the mass conditions.

    total : rp.ndarray
        The total mass of the system.
    rate_of_change : rp.ndarray
        The rate of change of mass.

    total_moment_of_inertia : rp.ndarray
        The total moment of inertia.

    breakdown : Conditions
        A nested Conditions object representing the breakdown of mass components.

    Notes
    -----
    All attributes are initialized using default factories to ensure each instance
    has its own copy of mutable objects.
    """

    # Attribute             Type    Default Value
    tag:                    str         = 'Mass Conditions'

    total:                  rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    rate_of_change:         rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    volume:                 rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    density:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    center_of_gravity:      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    moments_of_inertia:     rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3, 3)))

    breakdown:              Conditions  = field(default_factory=lambda: Conditions(tag='Mass Breakdown'))

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestMassConditions(unittest.TestCase):

    def setUp(self):
        self.mass_conditions = MassConditions()

    def test_default_values(self):
        self.assertEqual(self.mass_conditions.tag, 'Mass Conditions')
        np.testing.assert_array_equal(self.mass_conditions.total, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.mass_conditions.rate_of_change, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.mass_conditions.total_moment_of_inertia, rp.zeros((1, 1, 3)))
        self.assertIsInstance(self.mass_conditions.breakdown, Conditions)
        self.assertEqual(self.mass_conditions.breakdown.tag, 'Mass Breakdown')

    def test_custom_name(self):
        custom_mass = MassConditions(tag="Custom Mass Conditions")
        self.assertEqual(custom_mass.tag, "Custom Mass Conditions")

    def test_total_mass(self):
        self.mass_conditions.total = rp.array([[1000.0]])
        np.testing.assert_array_equal(self.mass_conditions.total, rp.array([[1000.0]]))

    def test_rate_of_change(self):
        self.mass_conditions.rate_of_change = -0.5
        np.testing.assert_array_equal(self.mass_conditions.rate_of_change, rp.array([[-0.5]]))

    def test_total_moment_of_inertia(self):
        moment = rp.array([[100.0, 200.0, 300.0]])
        self.mass_conditions.total_moment_of_inertia = moment
        np.testing.assert_array_equal(self.mass_conditions.total_moment_of_inertia, moment)

    def test_breakdown(self):
        self.mass_conditions.breakdown.fuel = rp.array([[500.0]])
        self.mass_conditions.breakdown.payload = rp.array([[200.0]])
        np.testing.assert_array_equal(self.mass_conditions.breakdown.fuel, rp.array([[500.0]]))
        np.testing.assert_array_equal(self.mass_conditions.breakdown.payload, rp.array([[200.0]]))

    def test_array_shapes(self):
        self.assertEqual(self.mass_conditions.total.shape, (1, 1))
        self.assertEqual(self.mass_conditions.rate_of_change.shape, (1, 1))
        self.assertEqual(self.mass_conditions.total_moment_of_inertia.shape, (1, 1, 3))


if __name__ == '__main__':
    unittest.main()
