# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

# package imports
import jax
import jax.numpy as jnp
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Component, MassProperties
from RCAIDE.Library.Attributes import AircraftClass, MediumRange
from RCAIDE.Library.Components.Energy.Networks import EnergyNetwork
from RCAIDE.Library.Components.Wings import Wing
from RCAIDE.Library.Components.Fuselages import Fuselage
from RCAIDE.Library.Components.Nacelles import Nacelle
from RCAIDE.Library.Components.Landing_Gear import LandingGear

# ----------------------------------------------------------------------------------------------------------------------
# Components
# ----------------------------------------------------------------------------------------------------------------------


class VehicleEnvelope(eqx.Module):
    # Attribute             Type        Default Value
    ultimate_load_factor:   float        = 0.0
    limit_load_factor:      float        = 0.0

# ----------------------------------------------------------------------------------------------------------------------
#  System
# ----------------------------------------------------------------------------------------------------------------------


class System(Component):

    tag: str = eqx.field(static=True, default='System')

    configurations: Component = eqx.field(default_factory=lambda: Component(tag='Configurations'))

# ----------------------------------------------------------------------------------------------------------------------
#  Aircraft
# ----------------------------------------------------------------------------------------------------------------------

class AircraftReferenceGeometry(eqx.Module):
    
    mean_aerodynamic_chord: jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    projected_span: jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    aerodynamic_center: jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    center_of_gravity: jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))


class AircraftMassProperties(MassProperties):

    max_takeoff         :float = 0.
    takeoff             :float = 0.
    operating_empty     :float = 0.
    max_zero_fuel       :float = 0.
    cargo               :float = 0.

class Aircraft(System):

    tag:                str = eqx.field(static=True, default='Aircraft')
    
    ac_class:           AircraftClass = eqx.field(static=True, default_factory=MediumRange)
    envelope:           VehicleEnvelope = eqx.field(static=True, default_factory=VehicleEnvelope)
    mass_properties:    AircraftMassProperties = eqx.field(default_factory=AircraftMassProperties) #type: ignore

    passengers:         int     = eqx.field(static=True, default=0)
    
    design_mach_number: float   = eqx.field(static=True, default=0.)
    design_range:       float   = eqx.field(static=True, default=0.)
    design_cruise_alt:  float   = eqx.field(static=True, default=0.)

    energy:         EnergyNetwork = eqx.field(default_factory=lambda: EnergyNetwork(tag="Energy"))
    
    wings:          Component = eqx.field(default_factory=lambda: Component(tag='Wings'))
    fuselages:      Component = eqx.field(default_factory=lambda: Component(tag='Fuselages'))
    nacelles:       Component = eqx.field(default_factory=lambda: Component(tag='Nacelles'))
    landing_gear:   Component = eqx.field(default_factory=lambda: Component(tag='Landing Gear'))

    reference_geometry:  AircraftReferenceGeometry = eqx.field(default_factory=AircraftReferenceGeometry)
    analysis_data:      dict = eqx.field(default_factory=dict)

    def add_subcomponent(
            self,
            subcomponent: Component,
    ):

        if isinstance(subcomponent, Wing):
            new_wings = self.wings.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda a: a.wings, self, new_wings)
        elif isinstance(subcomponent, Fuselage):
            new_fuses = self.fuselages.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda a: a.fuselages, self, new_fuses)
        elif isinstance(subcomponent, Nacelle):
            new_nacs = self.nacelles.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda a: a.nacelles, self, new_nacs)
        elif isinstance(subcomponent, LandingGear):
            new_LGs = self.landing_gear.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda a: a.landing_gear, self, new_LGs)
        else:
            return super(Aircraft, self).add_subcomponent(subcomponent)

    def get_all_components(self):
        return self.subcomponents + (
            self.energy,
            self.wings,
            self.fuselages,
            self.nacelles,
            self.landing_gear
        )


