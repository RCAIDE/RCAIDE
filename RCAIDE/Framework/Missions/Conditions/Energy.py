# RCAIDE/Framework/Missions/Conditions/Energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field

# package imports
import RNUMPY as rp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Energy Networks and Stores
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class EnergyStoreConditions(Conditions):
    """
    Represents the conditions of an energy store in a simulation.

    This class encapsulates various attributes related to the energy store,
    including its name, gravitational effects, and total energy.

    Attributes
    ----------
    name : str
        The name of the energy store. Default is 'Energy Store'.

    total_energy : rp.ndarray
        The total energy contained in the store.
        Shape: (1, 1). Default is a zero array.

    Notes
    -----
    This class inherits from the Conditions base class and uses the dataclass
    decorator with keyword-only arguments.
    """

    # Attribute         Type        Default Value
    tag:                str         = 'Energy Store'

    total_energy:       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class EnergyConverterConditions(Conditions):
    """
    Represents the conditions of an energy converter in a simulation.

    This class encapsulates various attributes related to the energy converter,
    including its name, efficiency, power output, thrust vector, and rotational properties.

    Attributes
    ----------
    name : str
        The name of the energy converter. Default is 'Energy Converter'.
    
    efficiency : rp.ndarray
        The efficiency of the energy converter.
    power : rp.ndarray
        The power output of the energy converter.
    
    thrust_vector : rp.ndarray
        The thrust vector produced by the energy converter.
    
    x_axis_rotation : rp.ndarray
        The rotation around the x-axis.
    y_axis_rotation : rp.ndarray
        The rotation around the y-axis.
    z_axis_rotation : rp.ndarray
        The rotation around the z-axis.

    Notes
    -----
    This class inherits from the Conditions base class and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

    # Attribute         Type        Default Value
    tag:                str         = 'Energy Converter'

    efficiency:         rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    power:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    thrust_vector:      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    x_axis_rotation:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    y_axis_rotation:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    z_axis_rotation:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    inputs:             Conditions  = field(default_factory=lambda: Conditions(tag='Energy Converter Inputs'))
    outputs:            Conditions  = field(default_factory=lambda: Conditions(tag='Energy Converter Outputs'))


# ----------------------------------------------------------------------------------------------------------------------
#  Battery Stores
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
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
    
    mass : rp.ndarray
        The mass of the battery cell. Default is a zero array.
    temperature : rp.ndarray
        The temperature of the battery cell. Default is a zero array.
    charge_throughput : rp.ndarray
        The cumulative charge that has passed through the battery. Default is a zero array.
    state_of_charge : rp.ndarray
        The current state of charge of the battery cell. Default is a zero array.

    Notes
    -----
    This class inherits from EnergyStoreConditions and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

    # Attribute                 Type        Default Value
    tag:                        str         = 'Battery Cell'

    cycle_in_day:               int         = 0
    resistance_growth_factor:   float       = 0.0
    capacity_fade_factor:       float       = 0.0

    mass:                       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    temperature:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    charge_throughput:          rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    state_of_charge:            rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
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
    
    mass : rp.ndarray
        The mass of the battery pack in kilograms (kg).
        Default is a zero array.
    temperature : rp.ndarray
        The temperature of the battery pack in degrees Celsius (°C).
        Default is a zero array.

    Notes
    -----
    This class inherits from EnergyStoreConditions and uses the dataclass
    decorator with keyword-only arguments. All numpy array attributes are
    initialized with zero values.
    """

    # Attribute             Type                    Default Value
    tag:                    str                     = 'Battery Pack'

    maximum_total_energy:   float                   = 0.0

    cell:                   BatteryCellConditions   = field(default_factory=lambda: BatteryCellConditions())

    mass:                   rp.ndarray              = field(default_factory=lambda: rp.zeros((1, 1)))
    temperature:            rp.ndarray              = field(default_factory=lambda: rp.zeros((1, 1)))


# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Stores
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
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

    mass : rp.ndarray
        The mass of the fuel in kilograms (kg).
        Default is a zero array.

    Notes
    -----
    This class uses the dataclass decorator with keyword-only arguments.
    The mass attribute is initialized as a zero-filled numpy array.
    """

    # Attribute         Type        Default Value
    tag:                str         = 'Fuel'

    mass:               rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class EnergyLineConditions(Conditions):

    converters: Conditions = field(default_factory=lambda: Conditions(tag='Energy Line Converters'))
    propulsors: Conditions = field(default_factory=lambda: Conditions(tag='Energy Line Converters'))
    stores:     Conditions = field(default_factory=lambda: Conditions(tag='Energy Line Stores'))


@chex.dataclass
class EnergyNetworkConditions(Conditions):

    """
    Represents the conditions of an energy network in a simulation.

    This class encapsulates various attributes related to the energy state,
    efficiency, power, and forces acting on an energy network.

    Attributes
    ----------
    name : str
        The name of the energy network. Default is 'Energy Network'.

    total_energy : rp.ndarray
        The total energy in the network.
    total_efficiency : rp.ndarray
        The overall efficiency of the network.

    throttle : rp.ndarray
        The throttle setting of the network.

    total_power : rp.ndarray
        The total power output of the network.
    total_force_vector : rp.ndarray
        The total force vector acting on the network.
    total_moment_vector : rp.ndarray
        The total moment vector acting on the network.

    Notes
    -----
    All numpy array attributes are initialized with zero values.
    """

    # Attribute             Type        Default Value
    tag:                    str         = 'Energy Network'

    total_energy:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    total_efficiency:       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    throttle:               rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    total_power:            rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    total_force_vector:     rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    total_moment_vector:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    lines:                  Conditions  = field(default_factory=lambda: Conditions(tag='Energy Network Lines'))
