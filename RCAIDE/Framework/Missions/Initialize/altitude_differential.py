# RCAIDE/Framework/Missions/Initialize/altitude_differential.py
# (c) Copyright 2025 Aerospace Research Community LLC#
# Created:  Sep 2025, J. Smart
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# Package Imports

import jax.numpy as jnp

# RCAIDE Imports

import RCAIDE.Framework as rcf

# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------


def initialize_altitude_differential(
    state: "rcf.State",
    settings: "rcf.Settings",
    system: "rcf.System"):

    """
    Framework version of initialize_altitude_differential
    
    See Also
    --------
    func_altitude_differential: 
        Functional implementation which this method calls.
    """

    # Unpack state inputs
    t = state.numerics.dimensionless.control_points
    I = state.numerics.dimensionless.integrate
    r = state.frames.inertial.position_vector
    v = state.frames.inertial.velocity_vector

    # Get altitude and time step
    dz = r[-1,2] - r[0,2]
    dt = jnp.dot(I[-1, :] * dz, 1/v[:, 2])

    # Rescale operator
    t = t * dt

    # Pack state outputes
    t_initial = state.frames.inertial.time[0, 0]
    state.frames.inertial.time[:, 0] = t_initial + t[:, 0]

    return state, settings, system
