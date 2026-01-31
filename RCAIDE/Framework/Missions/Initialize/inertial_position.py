# RCAIDE/Framework/Missions/Initialization/inertial_position.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Inertial Position
# ----------------------------------------------------------------------------------------------------------------------


def initialize_inertial_position(state: "rcf.State",
                                 system: "rcf.System",
                                 settings: "rcf.Settings",
                                 ):

    p_initial               = state.initials.frames.inertial.position_vector
    p_current               = state.frames.inertial.position_vector
    p_initial               = p_initial.at[-1, None, -1].set(-state.initials.freestream.altitude[-1, 0])
    delta_p                 = p_initial[-1, None, :] - p_current[0, None, :]

    R_initial               = state.initials.frames.inertial.system_range
    R_current               = state.frames.inertial.system_range
    delta_R                 = R_initial[-1, None, :] - R_current[0, None, :]

    state.frames.inertial.position_vector   += delta_p
    state.frames.inertial.system_range      += delta_R

    return state, system, settings

