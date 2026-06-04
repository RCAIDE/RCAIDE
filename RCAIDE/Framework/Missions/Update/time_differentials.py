# RCAIDE/Framework/Missions/Update/time_differentials.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Time Differentials
# ----------------------------------------------------------------------------------------------------------------------


def update_time_differentials(state: "rcf.State",
                              system: "rcf.System",
                              settings: "rcf.Settings",
                              ):

    x = state.numerics.dimensionless.control_points
    D = state.numerics.dimensionless.differentiate
    I = state.numerics.dimensionless.integrate

    time = state.frames.inertial.time
    T = time[-1] - time[0]
    t_scaled = x * T
    D_scaled = D / T
    I_scaled = I * T

    state = eqx.tree_at(lambda s: (s.numerics.time.control_points, s.numerics.time.differentiate, s.numerics.time.integrate), state,
                        (t_scaled, D_scaled, I_scaled), is_leaf=lambda x: x is None)

    return state, system, settings
