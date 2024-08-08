# RCAIDE/Framework/Missions/Update/angular_acceleration.py
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
#  angular_acceleration
# ----------------------------------------------------------------------------------------------------------------------


def update_angular_acceleration(State: rcf.State,
                                Settings: rcf.Settings,
                                System: rcf.System):

    w = State.frames.inertial.angular_velocity
    D = State.numerics.time.differentiate

    aa = np.dot(D, w)

    State.frames.inertial.angular_acceleration = aa
                   
    return State, Settings, System