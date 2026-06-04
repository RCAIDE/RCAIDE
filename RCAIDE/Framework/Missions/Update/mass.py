# RCAIDE/Framework/Missions/mass.py
# (c) Copyright 2026 Aerospace Research Community LLC#
# Created:  Jan 2026, E. Botero
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE Imports
import RCAIDE.Framework as rcf




# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------


def update_mass_and_weight(
    state: "rcf.State",
    system: "rcf.System",
    settings: "rcf.Settings",
):
    """
    Updates the current mass of the system
    """

    m0    = state.mass.total[0,0]
    mdot  = state.mass.rate_of_change
    I     = state.numerics.time.integrate
    g     = state.freestream.gravity

    # calculate
    m = m0 + jnp.dot(I, mdot )
    W = m*g

    # pack
    state = eqx.tree_at(
        lambda s:(
            s.mass.total,
            s.frames.inertial.gravity_force_vector
        ),
        state,
        (
            state.mass.total.at[1:,0].set(m[1:,0]),
            state.frames.inertial.gravity_force_vector.at[:,2].set(W[:,0])
        )
    )

    return state, system, settings