# RCAIDE/Framework/Missions/Initialization/time.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import RNUMPY as rp

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Time
# ----------------------------------------------------------------------------------------------------------------------


def initialize_time(state: "rcf.State",
                    system: "rcf.System",
                    settings: "rcf.Settings"
                    ):

    t_initial = state.initials.frames.inertial.time
    if rp.all(t_initial == None):
        t_initial = rp.atleast_2d(state.frames.planet.start_time)

    t_current = state.frames.inertial.time

    delta_t     = t_initial[-1, 0] - t_current[0, 0]
    offset_time = t_current + delta_t

    state.frames.planet.start_time  = t_initial
    state.frames.inertial.time      = offset_time

    return state, system, settings


