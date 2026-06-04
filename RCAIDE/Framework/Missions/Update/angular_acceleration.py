# RCAIDE/Framework/Missions/Update/angular_acceleration.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Angular Acceleration
# ----------------------------------------------------------------------------------------------------------------------


def update_angular_acceleration(state: "rcf.State",
                                system: "rcf.System",
                                settings: "rcf.Settings",
                                ):

    w = state.frames.inertial.angular_velocity_vector
    D = state.numerics.time.differentiate

    state = eqx.tree_at(lambda s:s.frames.inertial.angular_acceleration_vector, state, jnp.dot(D, w))
                   
    return state, system, settings