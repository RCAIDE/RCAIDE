# RCAIDE/Framework/Methods/Aerodynamics/VLM/pressure_coefficients.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Mar 2026, J. Smart
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING
import jax
import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  Compute VLM Pressure Coefficients
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
@jax.jit
def compute_pressure_coefficients(VD, v_total, Gamma, v_inf):
    """ 
    Computes the differential pressure coefficient (Delta C_P) for all panels.
    Input shapes: v_total (n_time, N, 3), GAMMA (n_time, N)
    """
    # Local Velocity Components (normalized by V_inf) ------------------------------------------------------------------
    Vx_local = v_total[:, :, 0] / v_inf
    Vy_local = v_total[:, :, 1] / v_inf
    
    # Local Panel Geometry (Sweep Tangents and Dihedral) ---------------------------------------------------------------
    dx = VD.chord_lengths
    strip_ids = jnp.cumsum(VD.is_leading_edge) - 1
    strip_chord_array = jax.ops.segment_sum(dx, strip_ids, num_segments=VD.total_strips)
    strip_chord = strip_chord_array[strip_ids]

    
    # Front edge sweep (Front-Left [0] to Front-Right [3])
    dx_A = VD.panel_vertices[:, 3, 0] - VD.panel_vertices[:, 0, 0]
    dy_A = VD.panel_vertices[:, 3, 1] - VD.panel_vertices[:, 0, 1]
    dz_A = VD.panel_vertices[:, 3, 2] - VD.panel_vertices[:, 0, 2]
    dy_z_A = jnp.maximum(jnp.sqrt(dy_A**2 + dz_A**2), 1e-12)  # Prevent DivByZero
    
    tan_A   = dx_A / dy_z_A
    cos_DL  = dy_A / dy_z_A  # Cosine of local dihedral
    
    # Back edge sweep (Back-Left [1] to Back-Right [2])
    dx_B = VD.panel_vertices[:, 2, 0] - VD.panel_vertices[:, 1, 0]
    dy_B = VD.panel_vertices[:, 2, 1] - VD.panel_vertices[:, 1, 1]
    dz_B = VD.panel_vertices[:, 2, 2] - VD.panel_vertices[:, 1, 2]
    dy_z_B = jnp.maximum(jnp.sqrt(dy_B**2 + dz_B**2), 1e-12)
    
    tan_B = dx_B / dy_z_B    

    # Helmholtz' theorem integration of anterior circulation from shed vortices ----------------------------------------

    def scan_fn(a, b):
        # a and b are tuples: (value, is_leading_edge_flag)
        v1, le1 = a
        v2, le2 = b
        # If element 'b' is a leading edge, it resets the sum to just v2
        return jnp.where(le2, v2, v1 + v2), le1 | le2

    gamma_over_c = Gamma / strip_chord[None, :]                                           # Circulation per unit chord
    is_le = jnp.broadcast_to(VD.is_leading_edge[None, :], gamma_over_c.shape)             # Broadcast the 1D LE flag to match the (n_time, N) matrix
    gamma_anterior, _ = jax.lax.associative_scan(scan_fn, (gamma_over_c, is_le), axis=1)  # Associative scan w/ binary switch on leading edge
    Gamma_anterior = jnp.where(is_le, 0.0, jnp.roll(gamma_anterior, shift=1, axis=1))
    
    # Sweep / Sideslip Correction --------------------------------------------------------------------------------------
    Gamma_lateral   = Gamma_anterior * (tan_A - tan_B)[None, :] - gamma_over_c * tan_B[None, :]
    dCp_sideslip    = 2.0 * Vy_local * cos_DL[None, :] * Gamma_lateral / dx[None, :]
    
    # Net Circulation --------------------------------------------------------------------------------------------------
    Gamma_net = Gamma * Vx_local / dx
    
    # Final Delta Cp
    dCp = 2.0 * Gamma_net + dCp_sideslip
    
    return dCp

# ---------------------------------------------------------
#  STATEFUL VERSION
# ---------------------------------------------------------
@inputs(
    "system.analysis_data['vortex_distribution']",
    "system.analysis_data['relative_velocity']",
    "system.analysis_data['vortex_strengths']",
    "state.freestream.speed"
)
@outputs("system.analysis_data['dCp']",)
def compute_panel_pressures(state: "State", system: "System", settings: "Settings"):
    """ Calculates the differential pressure coefficient (Delta C_P) for all VLM panels. """
    
    analysis = system.analysis_data
    VD = analysis["vortex_distribution"]
    
    v_total = analysis["relative_velocity"]
    GAMMA = analysis["vortex_strengths"]
    v_inf = state.freestream.speed
    
    dCp = compute_pressure_coefficients(VD, v_total, GAMMA, v_inf)
    
    updated_analysis_data = analysis | {"dCp": dCp}
    
    updated_system = eqx.tree_at(lambda s: s.analysis_data, system, updated_analysis_data)

    return state, updated_system, settings
