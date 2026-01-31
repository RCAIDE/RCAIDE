# RCAIDE/Framework/Missions/residuals.py
# (c) Copyright 2025 Aerospace Research Community LLC#
# Created:  Sep 2025, J. Smart
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# RCAIDE Imports

import RCAIDE.Framework as rcf


# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------


def flight_dynamics_residuals(
    state: "rcf.State",
    system: "rcf.System",
    settings: "rcf.Settings",
):
    """
    Calculates the residuals from the flight dynamics equations.
    """

    active_residuals = state.dynamics.get_active_residuals()
    force_residuals  = [res for res in active_residuals if res.type == 'force']
    moment_residuals = [res for res in active_residuals if res.type == 'moment']

    FT      = state.frames.inertial.total_force_vector
    MT      = state.frames.inertial.total_moment_vector
    a       = state.frames.inertial.acceleration_vector
    wdot    = state.frames.inertial.angular_acceleration_vector

    m   = state.mass.total
    I   = state.mass.moments_of_inertia

    for force_res in force_residuals:
        force_res.value = FT[:, force_res.index] / m[:, 0] - a[:, force_res.index]
    for moment_res in moment_residuals:
        if I[moment_res.index, moment_res.index] == 0:
            raise ValueError(f"Moment of Inertia Matrix must be defined for residual: {moment_res.tag} at "
                             f"I[{moment_res.index}, {moment_res.index}]")
        moment_res.value = MT[:, moment_res.index] / I[moment_res.index, moment_res.index] - wdot[:, moment_res.index]
        
    return state, system, settings