# RCAIDE/Framework/Methods/Aerodynamics/VLM/boundary_conditions.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Mar 2026, J. Smart
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING

import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings
    from RCAIDE.Framework.Analyses.Aerodynamics.VORJAX import VLMSettings
    from RCAIDE.Framework.Methods.Aerodynamics.VORJAX.vortex_distribution import VortexDistribution

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  VLM Boundary Conditions (Vortex Strength Right Hand Side Matrix)
# ----------------------------------------------------------------------------------------------------------------------


@inputs(
    "settings.analysis.aerodynamics: VLMSettings",
    "system.analysis_data['vortex_distribution']",
    "state.aerodynamics.angles.alpha",
    "state.aerodynamics.angles.beta",
    "state.freestream.speed",
    "state.stability.static.roll_rate",
    "state.stability.static.pitch_rate",
    "state.stability.static.yaw_rate"
)
@outputs(
    "system.analysis_data['boundary_conditions']",
    "system.analysis_data['relative_velocity']"
)
def compute_boundary_conditions(state: "State", system: "System", settings: "Settings"):
    """
    Computes the Neumann boundary condition (RHS) for the VLM.
    RHS = (V_freestream + V_rotation + V_wake) @ n
    """
    
    vlm_settings: "VLMSettings" = settings.analysis.aerodynamics  # type: ignore
    VD: VortexDistribution = system.analysis_data["vortex_distribution"]  # type: ignore
    
    # Extract State Conditions
    alpha = state.aerodynamics.angles.alpha
    beta  = state.aerodynamics.angles.beta
    v_inf = state.freestream.speed
    
    p = state.stability.static.roll_rate
    q = state.stability.static.pitch_rate
    r = state.stability.static.yaw_rate
    
    # Squeeze to drop the dummy dimension from the state vectors,
    # transpose to prepare for cross product -> (n_time, 3)
    omega = jnp.concatenate([p, q, r], axis=1)
    
    # Build Freestream Velocity Vector (Wind Speed in Body Frame)
    v_fs = v_inf * jnp.concatenate([
        jnp.cos(alpha) * jnp.cos(beta),
        jnp.sin(beta), 
        jnp.sin(alpha) * jnp.cos(beta)
    ], axis=1)
    
    # Compute Rotational Velocity at every control point: V_rot = -(Omega x r)
    moment_center = system.reference_geometry.center_of_gravity
    r_giro = VD.collocation_points - moment_center
    
    v_rot = -jnp.cross(omega[:, None, :], r_giro[None, :, :])
    
    # Sum the total relative velocity (N, 3)
    v_total = v_fs[:, None, :] + v_rot
    if vlm_settings.model_propeller_wake:
        # TODO: Convert BEMT and add wake calculation to VLM Process
        raise ValueError("Propeller wake modelling is unsupported pending BEMT inclusion in RCAIDE.")
        v_total = v_total + system.analysis_data["induced_wake"] #type: ignore
        
    # Take the Dot Product with the Panel Normals
    # Normalize by V_inf to match the standard VLM coefficient formulation
    v_unit = v_total / v_inf[:, None]
    
    # Dot product: -sum(V * N, axis=1)
    base_rhs_array = -jnp.sum(v_unit * VD.normal_vectors, axis=-1)

    # Camber correction from thin wing assumption
    v_unit_x = v_unit[..., 0]
    rhs_array = base_rhs_array + (v_unit_x * VD.camber_slopes)

    updated_analysis_data = system.analysis_data | {
        "boundary_conditions": rhs_array,
        "relative_velocity": v_total,
    }

    updated_system = eqx.tree_at(lambda s: s.analysis_data, system, updated_analysis_data)
    
    return state, updated_system, settings
