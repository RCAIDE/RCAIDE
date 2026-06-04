# RCAIDE/Framework/Missions/Initialization/inertial_position.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Inertial Position
# ----------------------------------------------------------------------------------------------------------------------


import equinox as eqx

def initialize_inertial_position(state: "rcf.State",
                                 system: "rcf.System",
                                 settings: "rcf.Settings",
                                 ):

    # Extract current arrays
    p_initial = state.initials.frames.inertial.position_vector
    p_current = state.frames.inertial.position_vector
    
    # Calculate deltas
    p_initial = p_initial.at[-1, None, -1].set(-state.initials.freestream.altitude[-1, 0])
    delta_p = p_initial[-1, None, :] - p_current[0, None, :]

    R_initial = state.initials.frames.inertial.system_range
    R_current = state.frames.inertial.system_range
    delta_R = R_initial[-1, None, :] - R_current[0, None, :]

    # Calculate the new values
    new_position_vector = p_current + delta_p
    new_system_range = R_current + delta_R

    state = eqx.tree_at(
        lambda s: (s.frames.inertial.position_vector, s.frames.inertial.system_range),
        state,
        (new_position_vector, new_system_range)
    )

    return state, system, settings

