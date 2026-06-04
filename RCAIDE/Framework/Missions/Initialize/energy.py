# RCAIDE/Framework/Missions/Initialization/energy.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE Imports
import RCAIDE.Framework as rcf
from RCAIDE.Framework.Missions.Conditions import Conditions
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyLineConditions as Line
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyStoreConditions as Store
from RCAIDE.Framework.Missions.Conditions.Energy import EnergyConverterConditions as Converter


# ----------------------------------------------------------------------------------------------------------------------
# Initialize Energy
# ----------------------------------------------------------------------------------------------------------------------

def _build_converter_tree(system_converter) -> "Converter":
    """Recursively builds the state Conditions tree to mirror the system structure."""
    
    # 1. Base Case: Create the state object for the current level
    # (Assuming 'Converter' is the correct state class here based on your snippet)
    state_node = Converter(tag=system_converter.tag)
    
    # 2. Recursive Step: Does this system component have sub-converters?
    if hasattr(system_converter, 'converters') and system_converter.converters:
        for sub_sys_conv in system_converter.converters:
            
            # Recurse down to build the child's entire tree
            built_child_state = _build_converter_tree(sub_sys_conv)
            
            # Attach the fully built child to the current node
            state_node = state_node.add_subcondition(built_child_state)
            
    return state_node


def initialize_energy(state: "rcf.State",
                      system: "rcf.Aircraft",
                      settings: "rcf.Settings",
                      ):

    for l_idx, line in enumerate(system.energy.lines):
        
        state = eqx.tree_at(lambda s: s.energy.lines, state, state.energy.lines.add_subcondition(Line(tag=line.tag)))
        
        # Grab the current, empty state container for this line's converters
        line_converters_state = state.energy.lines[l_idx].converters
        
        # Build each root converter's tree and attach it
        for root_sys_converter in line.converters:
            

            fully_built_root_state = _build_converter_tree(root_sys_converter)
            
            # Add the finished tree to the line's state container
            line_converters_state = line_converters_state.add_subcondition(fully_built_root_state)

        state = eqx.tree_at(
            lambda s: s.energy.lines[l_idx].converters, 
            state, 
            line_converters_state
        )

        for store in line.stores:
            state = eqx.tree_at(lambda s: s.energy.lines[l_idx].stores, state, state.energy.lines[l_idx].stores.add_subcondition(Store(tag=store.tag)))
        
        state = eqx.tree_at(lambda s: s.energy.lines[l_idx], state, state.energy.lines[l_idx].expand_rows(state.numerics.number_of_control_points))

    return state, system, settings
