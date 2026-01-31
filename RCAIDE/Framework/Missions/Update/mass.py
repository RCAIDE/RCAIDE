# RCAIDE/Framework/Missions/mass.py
# (c) Copyright 2026 Aerospace Research Community LLC#
# Created:  Jan 2026, E. Botero
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# RCAIDE Imports

import RCAIDE.Framework as rcf

import RNUMPY as rp


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
    m = m0 + rp.dot(I, mdot )
    W = m*g

    # pack
    state.mass.total = state.mass.total.at[1:,0].set(m[1:,0]) # m0 is the initial, so don't change it
    state.frames.inertial.gravity_force_vector = state.frames.inertial.gravity_force_vector.at[:,2].set(W[:,0])

    return state, system, settings