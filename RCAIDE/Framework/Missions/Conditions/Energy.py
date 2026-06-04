# RCAIDE/Framework/Missions/Conditions/Energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Energy Networks and Stores
# ----------------------------------------------------------------------------------------------------------------------


class EnergyStoreConditions(Conditions):

    # Attribute         Type        Default Value
    tag:                str         = eqx.field(static=True, default='Energy Store')

    total_energy:       jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))


class EnergyConverterConditions(Conditions):

    # Attribute         Type        Default Value
    tag:                str         = eqx.field(static=True, default='Energy Converter')

    efficiency:         jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    power:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))

    thrust_vector:      jnp.ndarray  = eqx.field(default_factory=lambda: jnp.zeros((1, 3)))

    x_axis_rotation:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    y_axis_rotation:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    z_axis_rotation:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))

    inputs:             Conditions  = eqx.field(default_factory=lambda: Conditions(tag='Energy Converter Inputs'))
    outputs:            Conditions  = eqx.field(default_factory=lambda: Conditions(tag='Energy Converter Outputs'))


# ----------------------------------------------------------------------------------------------------------------------
#  Battery Stores
# ----------------------------------------------------------------------------------------------------------------------


class BatteryCellConditions(EnergyStoreConditions):

    # Attribute                 Type        Default Value
    tag:                        str         = eqx.field(static=True, default='Battery Cell')

    cycle_in_day:               int         = eqx.field(static=True, default=0)
    resistance_growth_factor:   float       = eqx.field(static=True, default=0.0)
    capacity_fade_factor:       float       = eqx.field(static=True, default=0.0)

    mass:                       jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    temperature:                jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    charge_throughput:          jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    state_of_charge:            jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))


class BatteryPackConditions(EnergyStoreConditions):

    # Attribute             Type                    Default Value
    tag:                    str                     = eqx.field(static=True, default='Battery Pack')

    maximum_total_energy:   float                   = eqx.field(static=True, default=0.0)

    cell:                   BatteryCellConditions   = eqx.field(default_factory=BatteryCellConditions)

    mass:                   jnp.ndarray              = eqx.field(default_factory=lambda: jnp.empty(0))
    temperature:            jnp.ndarray              = eqx.field(default_factory=lambda: jnp.empty(0))


# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Stores
# ----------------------------------------------------------------------------------------------------------------------


class FuelConditions(EnergyStoreConditions):

    # Attribute         Type        Default Value
    tag:                str         = eqx.field(static=True, default='Fuel')

    mass:               jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))


class EnergyLineConditions(Conditions):

    converters: Conditions = eqx.field(default_factory=lambda: Conditions(tag='Energy Line Converters'))
    propulsors: Conditions = eqx.field(default_factory=lambda: Conditions(tag='Energy Line Converters'))
    stores:     Conditions = eqx.field(default_factory=lambda: Conditions(tag='Energy Line Stores'))


class EnergyNetworkConditions(Conditions):

    # Attribute             Type        Default Value
    tag:                    str         = eqx.field(static=True, default='Energy Network')

    total_energy:           jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    total_efficiency:       jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    
    throttle:               jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    total_power:            jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    
    total_force_vector:     jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    total_moment_vector:    jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    lines:                  Conditions  = eqx.field(default_factory=lambda: Conditions(tag='Energy Network Lines'))
