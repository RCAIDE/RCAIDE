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
    """
    Represents the conditions of an energy network in a simulation.

    This class encapsulates various attributes related to the energy state,
    efficiency, power, and forces acting on an energy network.

    Attributes
    ----------
    name : str
        The name of the energy network. Default is 'Energy Network'.
    
    total_energy : np.ndarray
        The total energy in the network.
    total_efficiency : np.ndarray
        The overall efficiency of the network.
    
    throttle : np.ndarray
        The throttle setting of the network.
    
    total_power : np.ndarray
        The total power output of the network.
    total_force_vector : np.ndarray
        The total force vector acting on the network.
    total_moment_vector : np.ndarray
        The total moment vector acting on the network.

    Notes
    -----
    All numpy array attributes are initialized with zero values.
    """

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
    """
    Represents the conditions of an energy store in a simulation.

    This class encapsulates various attributes related to the energy store,
    including its name, gravitational effects, and total energy.

    Attributes
    ----------
    name : str
        The name of the energy store. Default is 'Energy Store'.

    total_energy : np.ndarray
        The total energy contained in the store.
        Shape: (1, 1). Default is a zero array.

    Notes
    -----
    This class inherits from the Conditions base class and uses the dataclass
    decorator with keyword-only arguments.
    """

    # Attribute         Type        Default Value
    name:               str         = 'Energy Store'

    total_energy:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class EnergyConverterConditions(Conditions):
    """
    Represents the conditions of an energy converter in a simulation.

    This class encapsulates various attributes related to the energy converter,
    including its name, efficiency, power output, thrust vector, and rotational properties.

    Attributes
    ----------
    name : str
        The name of the energy converter. Default is 'Energy Converter'.
    
    efficiency : np.ndarray
        The efficiency of the energy converter.
    power : np.ndarray
        The power output of the energy converter.
    
    thrust_vector : np.ndarray
        The thrust vector produced by the energy converter.
    
    x_axis_rotation : np.ndarray
        The rotation around the x-axis.
    y_axis_rotation : np.ndarray
        The rotation around the y-axis.
    z_axis_rotation : np.ndarray
        The rotation around the z-axis.

    Notes
    -----
    This class inherits from the Conditions base class and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

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
    """
    Represents the conditions of a battery cell in a simulation.

    This class encapsulates various attributes related to a battery cell,
    including its name, cycling information, degradation factors, and physical properties.

    Attributes
    ----------
    name : str
        The name of the battery cell. Default is 'Battery Cell'.
    
    cycle_in_day : int
        The number of charge/discharge cycles completed in a day. Default is 0.
    resistance_growth_factor : float
        Factor representing the increase in internal resistance over time. Default is 0.0.
    capacity_fade_factor : float
        Factor representing the decrease in battery capacity over time. Default is 0.0.
    
    mass : np.ndarray
        The mass of the battery cell. Default is a zero array.
    temperature : np.ndarray
        The temperature of the battery cell. Default is a zero array.
    charge_throughput : np.ndarray
        The cumulative charge that has passed through the battery. Default is a zero array.
    state_of_charge : np.ndarray
        The current state of charge of the battery cell. Default is a zero array.

    Notes
    -----
    This class inherits from EnergyStoreConditions and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

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
    """
    Represents the conditions of a battery pack in a simulation.

    This class encapsulates various attributes related to a battery pack,
    including its name, maximum total energy, cell conditions, mass, and temperature.

    Attributes
    ----------
    name : str
        The name of the battery pack. Default is 'Battery Pack'.
    
    maximum_total_energy : float
        The maximum total energy capacity of the battery pack in watt-hours (Wh).
        Default is 0.0.
    
    cell : BatteryCellConditions
        An instance of BatteryCellConditions representing the conditions of a 
        single cell in the battery pack. Default is a new BatteryCellConditions instance.
    
    mass : np.ndarray
        The mass of the battery pack in kilograms (kg).
        Default is a zero array.
    temperature : np.ndarray
        The temperature of the battery pack in degrees Celsius (°C).
        Default is a zero array.

    Notes
    -----
    This class inherits from EnergyStoreConditions and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

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
    """
    Represents the conditions of a fuel energy store in a simulation.

    This class encapsulates attributes related to fuel storage, including
    its name and mass. It inherits from EnergyStoreConditions and uses
    keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the fuel store. Default is 'Fuel'.

    mass : np.ndarray
        The mass of the fuel in kilograms (kg).
        Default is a zero array.

    Notes
    -----
    This class uses the dataclass decorator with keyword-only arguments.
    The mass attribute is initialized as a zero-filled numpy array.
    """

    # Attribute         Type        Default Value
    name:               str         = 'Fuel'

    mass:               np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

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
        np.testing.assert_array_equal(self.network.total_force_vector, np.zeros((1, 1, 3)))
        np.testing.assert_array_equal(self.network.total_moment_vector, np.zeros((1, 1, 3)))


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
        np.testing.assert_array_equal(self.converter.thrust_vector, np.zeros((1, 1, 3)))
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
