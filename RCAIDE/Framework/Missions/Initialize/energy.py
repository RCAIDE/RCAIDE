# RCAIDE/Framework/Missions/Initialization/energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import RNUMPY as rp

# RCAIDE Imports
import RCAIDE.Framework as rcf
from RCAIDE.Framework.Missions.Conditions import Conditions
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyLineConditions as Line
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyStoreConditions as Store
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyConverterConditions as Converter


# ----------------------------------------------------------------------------------------------------------------------
# Initialize Energy
# ----------------------------------------------------------------------------------------------------------------------


def initialize_energy(state: "rcf.State",
                      system: "rcf.Aircraft",
                      settings: "rcf.Settings",
                      ):

    state.energy.lines._attributes_frozen = False

    for l_idx, line in enumerate(system.energy.lines):
        state.energy.lines[l_idx] = Line(tag=line.tag)
        for p_idx, propulsor in line.propulsors:
            state.energy.lines[l_idx].propulsors[p_idx] = Converter()
            state.energy.lines[l_idx].propulsors[p_idx].propulsors = Converter(tag=propulsor.tag)
            for converter in propulsor.converters:
                state.energy.lines[l_idx].propulsors[p_idx].propulsors[converter.get_field_name()] = Converter(tag=converter.tag)
        for store in line.stores:
            state.energy.lines[l_idx].stores._attributes_frozen = False
            state.energy.lines[l_idx].stores[store.get_field_name()] = Store(tag=store.tag)
            state.energy.lines[l_idx].stores._attributes_frozen = True

    state.energy.lines._attributes_frozen = True


    def _recursive_initialize_energy(conditions: Conditions, initial_conditions: Conditions):

        for k, v in vars(conditions).items():

            if isinstance(v, rp.ndarray):
                v[:, 0] = vars(initial_conditions)[k][-1, 0]
            elif isinstance(v, int) or isinstance(v, float):
                v = vars(initial_conditions)[k]
            if isinstance(v, Conditions):
                _recursive_initialize_energy(v, vars(initial_conditions)[k])

    _recursive_initialize_energy(state.energy, state.initials.energy)

    return state, system, settings
