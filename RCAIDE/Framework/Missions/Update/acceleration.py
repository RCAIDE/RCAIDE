# RCAIDE/Framework/Missions/Update/acceleration.py
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
#  acceleration
# ----------------------------------------------------------------------------------------------------------------------


def update_acceleration(state: "rcf.State",
                        system: "rcf.System",
                        settings: "rcf.Settings"):

    v = state.frames.inertial.velocity_vector
    D = state.numerics.time.differentiate

    state = eqx.tree_at(lambda s: s.frames.inertial.acceleration_vector, state, jnp.dot(D, v))
                   
    return state, system, settings
