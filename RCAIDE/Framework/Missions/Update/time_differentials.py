# RCAIDE/Framework/Missions/Update/time_differentials.py
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
#  Update Time Differentials
# ----------------------------------------------------------------------------------------------------------------------


def update_time_differentials(State: rcf.State,
                              Settings: rcf.Settings,
                              System: rcf.System):

    x = State.numerics.dimensionless.control_points
    D = State.numerics.dimensionless.differentiate
    I = State.numerics.dimensionless.integrate

    time = State.frames.inertial.time
    T = time[-1] - time[0]
    t_scaled = x * T
    D_scaled = D / T
    I_scaled = I * T

    State.numerics.time.control_points  = t_scaled
    State.numerics.time.differentiate   = D_scaled
    State.numerics.time.integrate       = I_scaled

    return State, Settings, System
