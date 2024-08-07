# RCAIDE/Framework/Missions/Conditions/Propulsion.py
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
#  Propulsion
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class PropulsionConditions(Conditions):

    # Attribute             Type        Default Value
    name:                   str         = 'Propulsion'
    reverse_thrust_ratio:   float       = 0.0

    throttle:               np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    thrust_breakdown:       Conditions  = Conditions(name='Thrust Breakdown')


@dataclass(kw_only=True)
class BatteryPropulsionConditions(PropulsionConditions):

    #Attribute                  Type        Default Value
    name:                       str         = 'Battery Propulsion'

    cycle_day:                  int         = 0
    resistance_growth_factor:   float       = 1.0
    capacity_fade_factor:       float       = 1.0

    energy:                     np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    state_of_charge:            np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    voltage_under_load:         np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    voltage_open_circuit:       np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    cell_temperature:           np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    pack_temperature:           np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    cell_charge_throughput:     np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    propeller_y_axis_rotation:  np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    lift_rotor_y_axis_rotation: np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

