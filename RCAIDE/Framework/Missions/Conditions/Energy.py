# RCAIDE/Framework/Missions/Conditions/Energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

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
#  Energy Networks and Stores
# ----------------------------------------------------------------------------------------------------------------------


@dataclass
class NetworkConditions(Conditions):

    # Attribute             Type        Default Value
    name:                   str         = 'Energy Network'

    total_energy:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    total_efficiency:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    throttle:               np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    total_power:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    total_force_vector:     np.ndarray  = field(default_factory=lambda: np.zeros((1, 1, 3)))
    total_moment_vector:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1, 3)))


@dataclass(kw_only=True)
class EnergyStoreConditions(Conditions):

    # Attribute         Type        Default Value
    name:               str         = 'Energy Store'

    gravity:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    total_energy:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class EnergyConverterConditions(Conditions):

    # Attribute         Type        Default Value
    name:               str         = 'Energy Converter'

    efficiency:         np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    power:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    thrust_vector:      np.ndarray  = field(default_factory=lambda: np.zeros((1, 1, 3)))

    x_axis_rotation:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    y_axis_rotation:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    z_axis_rotation:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


# ----------------------------------------------------------------------------------------------------------------------
#  Battery Stores
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class BatteryCellConditions(EnergyStoreConditions):

    # Attribute                 Type        Default Value
    name:                       str         = 'Battery Cell'

    cycle_in_day:               int         = 0
    resistance_growth_factor:   float       = 0.0
    capacity_fade_factor:       float       = 0.0

    mass:                       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    temperature:                np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    charge_throughput:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    state_of_charge:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class BatteryPackConditions(EnergyStoreConditions):

    # Attribute             Type                    Default Value
    name:                   str                     = 'Battery Pack'

    maximum_total_energy:   float                   = 0.0

    cell:                   BatteryCellConditions   = field(default_factory=lambda: BatteryCellConditions())

    mass:                   np.ndarray              = field(default_factory=lambda: np.zeros((1, 1)))
    temperature:            np.ndarray              = field(default_factory=lambda: np.zeros((1, 1)))


# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Stores
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class FuelConditions(EnergyStoreConditions):

    # Attribute     Type        Default Value
    name:           str         = 'Fuel'

    mass:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestNetworkConditions(unittest.TestCase):
    def setUp(self):
        self.network = NetworkConditions()

    def test_default_values(self):
        self.assertEqual(self.network.name, 'Energy Network')
        np.testing.assert_array_equal(self.network.total_energy, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.network.total_efficiency, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.network.throttle, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.network.total_power, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.network.total_force_vector, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.network.total_moment_vector, np.zeros((1, 3)))


class TestEnergyStoreConditions(unittest.TestCase):
    def setUp(self):
        self.store = EnergyStoreConditions()

    def test_default_values(self):
        self.assertEqual(self.store.name, 'Energy Store')
        np.testing.assert_array_equal(self.store.gravity, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.store.total_energy, np.zeros((1, 1)))


class TestEnergyConverterConditions(unittest.TestCase):
    def setUp(self):
        self.converter = EnergyConverterConditions()

    def test_default_values(self):
        self.assertEqual(self.converter.name, 'Energy Converter')
        np.testing.assert_array_equal(self.converter.efficiency, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.converter.power, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.converter.thrust_vector, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.converter.x_axis_rotation, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.converter.y_axis_rotation, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.converter.z_axis_rotation, np.zeros((1, 1)))


class TestBatteryCellConditions(unittest.TestCase):
    def setUp(self):
        self.cell = BatteryCellConditions()

    def test_default_values(self):
        self.assertEqual(self.cell.name, 'Battery Cell')
        self.assertEqual(self.cell.cycle_in_day, 0)
        self.assertEqual(self.cell.resistance_growth_factor, 0.0)
        self.assertEqual(self.cell.capacity_fade_factor, 0.0)
        np.testing.assert_array_equal(self.cell.mass, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.cell.temperature, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.cell.charge_throughput, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.cell.state_of_charge, np.zeros((1, 1)))


class TestBatteryPackConditions(unittest.TestCase):
    def setUp(self):
        self.pack = BatteryPackConditions()

    def test_default_values(self):
        self.assertEqual(self.pack.name, 'Battery Pack')
        self.assertEqual(self.pack.maximum_total_energy, 0.0)
        self.assertIsInstance(self.pack.cell, BatteryCellConditions)
        np.testing.assert_array_equal(self.pack.mass, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.pack.temperature, np.zeros((1, 1)))


class TestFuelConditions(unittest.TestCase):
    def setUp(self):
        self.fuel = FuelConditions()

    def test_default_values(self):
        self.assertEqual(self.fuel.name, 'Fuel')
        np.testing.assert_array_equal(self.fuel.mass, np.zeros((1, 1)))


if __name__ == '__main__':
    unittest.main()
