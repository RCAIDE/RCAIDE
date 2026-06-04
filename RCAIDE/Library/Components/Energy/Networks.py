# RCAIDE/Library/Components/Energy/Network.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from __future__ import annotations
from typing import TYPE_CHECKING

# package imports
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Component
from RCAIDE.Library.Components.Energy.Propulsors import Propulsor
from RCAIDE.Library.Components.Energy.Converters import EnergyConverter
from RCAIDE.Library.Components.Energy.Stores import EnergyStore

if TYPE_CHECKING:
    from RCAIDE.Framework import State, System, Settings
# ----------------------------------------------------------------------------------------------------------------------
#  Network
# ----------------------------------------------------------------------------------------------------------------------


class EnergyLine(Component):

    propulsors:     Component = eqx.field(default_factory=lambda: Component(tag='Propulsors'))
    converters:     Component = eqx.field(default_factory=lambda: Component(tag='Converters'))
    stores:         Component = eqx.field(default_factory=lambda: Component(tag='Stores'))

    def add_subcomponent(
            self,
            subcomponent: Component,
    ):

        if isinstance(subcomponent, Propulsor):
            new_props = self.propulsors.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda e: e.propulsors, self, new_props)
        elif isinstance(subcomponent, EnergyConverter):
            new_convs = self.converters.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda e: e.converters, self, new_convs)
        elif isinstance(subcomponent, EnergyStore):
            new_stores = self.stores.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda e: e.stores, self, new_stores)
        else:
            return super(EnergyLine, self).add_subcomponent(subcomponent)

    @staticmethod
    def calculate_performance(
        state: State,
        system: System,
        settings: Settings
    ):

        raise NotImplementedError('Subclasses must implement this method')


class EnergyNetwork(Component):

    tag: str = eqx.field(static=True, default='Energy Network')

    efficiency: float = 1.0

    lines: Component = eqx.field(default_factory=lambda: Component(tag='Lines'))


    @staticmethod
    def calculate_performance(state: State,
                              system: System,
                              settings: Settings
                              ):

        for line in system.energy.lines.subcomponents: #type: ignore
            line: EnergyLine
            state, system, settings = line.calculate_performance(state, system, settings)

        return state, system, settings

