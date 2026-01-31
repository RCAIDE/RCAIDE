# RCAIDE/Framework/Missions/Update/acceleration.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import RNUMPY as rp

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  acceleration
# ----------------------------------------------------------------------------------------------------------------------


def update_acceleration(state: "rcf.State",
                        system: "rcf.System",
                        settings: "rcf.Settings"):

    v = state.frames.inertial.velocity_vector
    D = state.numerics.time.differentiate

    a = rp.dot(D, v)

    state.frames.inertial.acceleration_vector = a
                   
    return state, system, settings
