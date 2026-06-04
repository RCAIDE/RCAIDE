# RCAIDE/Framework/Methods/Aerodynamics/VLM/vortex_strength.py
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

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  Compute VLM Vortex Strength
# ----------------------------------------------------------------------------------------------------------------------


@inputs(
    "system.analysis_data['vortex_distribution']",
    "system.analysis_data['VICs']",
    "system.analysis_data['boundary_conditions']",
    "system.analysis_data['singularities']",
)
@outputs(
    "system.analysis_data['vortex_strengths']",
)
def compute_vortex_strength(state: "State", system: "System", settings: "Settings"):
    """ Solves the linear system A * GAMMA = RHS for the vortex strengths. """
    
    analysis: dict[str, jnp.ndarray] = system.analysis_data
    VD = analysis["vortex_distribution"]
    
    # Extract the arrays we built in previous steps
    # C_mn shape: (n_time, receiver_N, sender_N, 3)
    C_mn = analysis["VICs"]
    
    # RHS shape: (n_time, receiver_N)
    RHS = analysis["boundary_conditions"]
    
    # RFLAG shape: (n_time, receiver_N)
    singularity_flag = analysis["singularities"]
    
    # Zero out the RHS for supersonic panels swept parallel to the Mach cone
    RHS = RHS * singularity_flag
    
    # Build the 'A' matrix via Dot Product: sum(C_mn * n)
    # The normal vector belongs to the RECEIVING panel (dim 1). 
    # We broadcast it over n_time (dim 0) and the sending panels (dim 2).
    # VD.normal_vectors shape: (N, 3) -> Broadcast to (1, N, 1, 3)
    normals_broadcast = VD.normal_vectors[None, :, None, :]
    
    # A shape: (n_time, receiver_N, sender_N)
    A = jnp.sum(C_mn * normals_broadcast, axis=-1)
    
    # Solve the linear system
    # A is (n_time, N, N), RHS is (n_time, N)
    # Output GAMMA is perfectly shaped as (n_time, N)
    GAMMA = jnp.linalg.solve(A, RHS[..., None]).squeeze(-1)
    
    # Pack the results
    updated_analysis_data = analysis | {"vortex_strengths": GAMMA}
    
    updated_system = eqx.tree_at(lambda s: s.analysis_data, system, updated_analysis_data)

    return state, updated_system, settings
