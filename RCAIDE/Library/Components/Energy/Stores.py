# RCAIDE/Library/Components/Energy/Stores.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May, 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Component, MassProperties

# ----------------------------------------------------------------------------------------------------------------------
# Energy Store
# ----------------------------------------------------------------------------------------------------------------------


class EnergyStore(Component):

    name: str = eqx.field(static=True, default='Energy Store')

    max_energy: float = 0.0

    specific_energy: float = 0.0
    specific_volume: float = 0.0

# ----------------------------------------------------------------------------------------------------------------------
# Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------

class FuelTankMass(MassProperties):

    full_fuel_mass: float = 0.0
    full_fuel_volume: float = 0.0

class FuelTank(EnergyStore):

    name = 'Fuel Tank'

    fuel_selector_ratio: float = 1.0
    secondary_fuel_flow: float = 0.0

    mass_properties: FuelTankMass = eqx.field(default_factory=FuelTankMass) #type: ignore

# ----------------------------------------------------------------------------------------------------------------------
# Battery
# ----------------------------------------------------------------------------------------------------------------------


class BatteryRagoneParameters(eqx.Module):

    const_1: float = 0.0
    const_2: float = 0.0
    lower_bound: float = 0.0
    i: float = 0.0


class Battery(EnergyStore):

    tag: str = eqx.field(static=True, default='Battery')

    max_energy:     float = 0.0
    max_power:      float = 0.0
    max_voltage:    float = 0.0

    resistance:     float = 0.0

    ragone: BatteryRagoneParameters = eqx.field(default_factory=BatteryRagoneParameters)