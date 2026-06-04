# RCAIDE/Framework/Missions/Update/freestream.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
if TYPE_CHECKING:
    from RCAIDE.Framework import State, System, Settings

# ----------------------------------------------------------------------------------------------------------------------
#  Update Freestream
# ----------------------------------------------------------------------------------------------------------------------


def update_freestream(state: "State",
                      system: "System",
                      settings: "Settings",
                      ):


    # Update Altitude
    alt = -state.frames.inertial.position_vector[:, 2][:, None] # Z is negative by right hand rule convention
    state = eqx.tree_at(lambda s:s.freestream.altitude, state, alt)

    # Update gravity
    G = state.freestream.planet.compute_gravity()
    state = eqx.tree_at(lambda s:s.freestream.gravity, state, state.freestream.gravity.at[:,0].set(G))

    # Update Atmospheric Properties
    atmo = state.freestream.atmosphere
    r = atmo.compute_density(alt)
    P = atmo.compute_pressure(alt)
    T = atmo.compute_temperature(alt)
    a = atmo.compute_speed_of_sound(alt)
    m = atmo.compute_dynamic_viscosity(alt)
    g = atmo.compute_gamma(alt)
    Cp = atmo.compute_Cp(alt)

    updated_fs = eqx.tree_at(lambda f:(
        f.density,
        f.pressure,
        f.temperature,
        f.speed_of_sound,
        f.dynamic_viscosity,
        f.gamma,
        f.Cp
        ),
        state.freestream,(
        r,
        P,
        T,
        a,
        m,
        g,
        Cp,
        )
    )
    state = eqx.tree_at(lambda s: s.freestream, state, updated_fs)

    # Speed
    v = state.frames.inertial.velocity_vector
    v_mag_sq = jnp.sum(v ** 2, axis=1)[:, None]
    v_mag    = jnp.sqrt(v_mag_sq)

    # Dynamic Pressure
    q = 0.5 * r * v_mag_sq

    # Mach Number
    M = v_mag / a

    # Stagnation
    P_t = P * (1 + (g - 1)/2 * M**2) ** (g / (g - 1))   # Stagnation Pressure
    T_t = T * (1 + (g - 1)/2 * M**2)                    # Stagnation Temperature

    # Reynolds Number (per meter)
    Re = r * v_mag / m

    state = eqx.tree_at(lambda s:(
        s.freestream.speed,
        s.freestream.mach_number,
        s.freestream.reynolds_number,
        s.freestream.dynamic_pressure,
        s.freestream.stagnation_pressure,
        s.freestream.stagnation_temperature,
        ), 
        state, (
        v_mag,
        M,
        Re,
        q,
        P_t,
        T_t,
        )
    )
                   
    return state, system, settings