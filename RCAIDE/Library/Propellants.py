# RCAIDE/Library/Propellants.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE imports
import RCAIDE.Library as rcl

# ----------------------------------------------------------------------------------------------------------------------
#  Propellants
# ----------------------------------------------------------------------------------------------------------------------


class MaxPropellantMassFractions(eqx.Module):

    Air:    float = eqx.field(static=True, default=0.0)
    O2:     float = eqx.field(static=True, default=0.0)


class PropellantTemperatures(eqx.Module):

    flash:          float = eqx.field(static=True, default=0.0)
    autoignition:   float = eqx.field(static=True, default=0.0)
    freeze:         float = eqx.field(static=True, default=0.0)
    boiling:        float = eqx.field(static=True, default=0.0)


class Propellant(eqx.Module):

    tag: str = eqx.field(static=True, default='Propellant')

    oxidizer: rcl.Gases.Gas = eqx.field(default_factory=rcl.Gases.Gas)

    density:            float = eqx.field(static=True, default=0.0)
    specific_energy:    float = eqx.field(static=True, default=0.0)
    energy_density:     float = eqx.field(static=True, default=0.0)

    max_mass_fraction:  MaxPropellantMassFractions  = eqx.field(default_factory=MaxPropellantMassFractions)
    temperatures:       PropellantTemperatures      = eqx.field(default_factory=PropellantTemperatures)


def _JetAFractions():
    return MaxPropellantMassFractions(
        Air=0.0633,
        O2=0.3022
    )

def _JetATemperatures():
    return PropellantTemperatures(
        flash=311.15,
        autoignition=483.15,
        freeze=233.15,
        boiling=0.0
    )

class JetA(Propellant):

    oxidizer: rcl.Gases.Gas = eqx.field(default_factory=rcl.Gases.O2)

    density         : float = eqx.field(static=True, default=820.)
    specific_energy : float = eqx.field(static=True, default=43.02e6)
    energy_density  : float = eqx.field(static=True, default=35276.4e6)

    max_mass_fraction   : MaxPropellantMassFractions = eqx.field(static=True, default_factory=_JetAFractions)

    temperatures        : PropellantTemperatures = eqx.field(static=True, default_factory=_JetATemperatures)

