# RCAIDE/Framework/Missions/Update/freestream.py
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
#  Update Freestream
# ----------------------------------------------------------------------------------------------------------------------


def update_freestream(state: "rcf.State",
                      system: "rcf.System",
                      settings: "rcf.Settings",
                      ):

    v = state.frames.inertial.velocity_vector
    r = state.freestream.density
    a = state.freestream.speed_of_sound
    m = state.freestream.dynamic_viscosity
    P = state.freestream.pressure
    T = state.freestream.temperature

    gamma   = rp.polyval(rp.array(state.freestream.atmosphere.fluid.gamma_coefficients), T)
    Cp      = rp.polyval(rp.array(state.freestream.atmosphere.fluid.cp_coefficients), T)

    # Speed
    v_mag_sq = rp.sum(v ** 2, axis=1)[:, None]
    v_mag    = rp.sqrt(v_mag_sq)

    # Dynamic Pressure
    q = 0.5 * r * v_mag_sq

    # Mach Number
    M = v_mag / a

    # Stagnation
    P_t = P * (1 + (gamma - 1)/2 * M**2) ** (gamma / (gamma - 1))   # Stagnation Pressure
    T_t = T * (1 + (gamma - 1)/2 * M**2)                            # Stagnation Temperature

    # Reynolds Number (per meter)
    Re = r * v_mag / m

    state.freestream.gamma                  = gamma
    state.freestream.Cp                     = Cp
    state.freestream.speed                  = v_mag
    state.freestream.mach_number            = M
    state.freestream.reynolds_number        = Re
    state.freestream.dynamic_pressure       = q
    state.freestream.stagnation_pressure    = P_t
    state.freestream.stagnation_temperature = T_t
                   
    return state, system, settings