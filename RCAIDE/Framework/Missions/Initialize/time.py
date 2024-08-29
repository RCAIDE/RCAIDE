# RCAIDE/Framework/Missions/Initialization/time.py
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
# Initialize Time
# ----------------------------------------------------------------------------------------------------------------------


def initialize_time(State: rcf.State,
                    Settings: rcf.Settings,
                    System: rcf.System):

    t_initial = State.initials.frames.inertial.time
    if not any(t_initial):
        t_initial = np.atleast_2d(State.frames.planet.start_time)

    t_current = State.frames.inertial.time

    delta_t     = t_initial[-1, 0] - t_current[0, 0]
    offset_time = t_current + delta_t

    State.frames.planet.start_time  = t_initial
    State.frames.inertial.time      = offset_time

    return State, Settings, System


