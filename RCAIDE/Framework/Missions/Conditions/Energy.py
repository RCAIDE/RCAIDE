# RCAIDE/Framework/Missions/Conditions/Energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

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

    # Attribute         Type        Default Value
    name:               str         = 'Energy Network'

    total_energy:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    total_efficiency:   np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    throttle:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    total_power:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    total_force:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))
    total_moment:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))


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

    thrust:             np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

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

    cell:                   BatteryCellConditions   = BatteryCellConditions()

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
