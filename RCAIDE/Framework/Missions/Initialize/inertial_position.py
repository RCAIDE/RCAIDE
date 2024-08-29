# RCAIDE/Framework/Missions/Initialization/inertial_position.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import numpy as np

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Inertial Position
# ----------------------------------------------------------------------------------------------------------------------


def initialize_inertial_position(State: rcf.State,
                                 Settings: rcf.Settings,
                                 System: rcf.System):

    p_initial               = State.initials.frames.inertial.position
    p_current               = State.frames.inertial.position
    p_initial[-1, None, -1] = -State.initials.freestream.altitude[-1, 0]
    delta_p                 = p_initial[-1, None, :] - p_current[0, None, :]

    R_initial               = State.initials.frames.inertial.system_range
    R_current               = State.frames.inertial.system_range
    delta_R                 = R_initial[-1, None, :] - R_current[0, None, :]

    State.frames.inertial.position      += delta_p
    State.frames.inertial.system_range  += delta_R

    return State, Settings, System

