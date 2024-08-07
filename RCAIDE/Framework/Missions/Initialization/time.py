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
# Imports
# ----------------------------------------------------------------------------------------------------------------------
# -
def time(State: rcf.State, Settings: rcf.Settings, System: rcf.System):

    try:
        t_initial = segment.initial_state.frames.inertial.time
    except:
        t_initial = np.atleast_2d(segment.current_state.frames.planet.start_time)

    t_current = segment.state.frames.inertial.time

    delta_t     = t_initial[-1, 0] - t_current[0, 0]
    offset_time = t_current + delta_t


