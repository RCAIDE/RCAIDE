# RCAIDE/Framework/Missions/Update/acceleration.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  acceleration
# ----------------------------------------------------------------------------------------------------------------------


def update_acceleration(State: rcf.State,
                        Settings: rcf.Settings,
                        System: rcf.System):

    v = State.frames.inertial.velocity
    D = State.numerics.time.differentiate

    a = np.dot(D, v)

    State.frames.inertial.acceleration = a
                   
    return State, Settings, System
