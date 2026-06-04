# RCAIDE/Library/Methods/Aerodynamics/transonic_spline.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: May 2026, J. Smart
# Modified: May 2026, J. Smart

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

# ----------------------------------------------------------------------------------------------------------------------
#  Transonic Spline
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# 1. PURE LIBRARY FUNCTION (Math Only)
# ---------------------------------------------------------
@jax.jit
def transonic_spline(M, M_sub, M_sup, val_sub, val_sup, grad_sub, grad_sup):
    """
    Calculates a cubic hermite spline for blending subsonic and supersonic results, including peak at Mach 1.0

    M_test: The target Mach number inside the transonic zone
    M_sub, M_sup: The boundary Mach numbers (e.g., 0.85, 1.15)
    val_sub, val_sup: The value evaluated at M_sub and M_sup
    grad_sub, grad_sup: gradient w.r.t. Mach evaluated at M_sub and M_sup
    """
    # Normalized transition parameter [0, 1]
    t = (M - M_sub) / (M_sup - M_sub)
    delta_M = M_sup - M_sub
    
    # Hermite Basis Functions
    h00 = 2.0 * t**3 - 3.0 * t**2 + 1.0
    h10 = t**3 - 2.0 * t**2 + t
    h01 = -2.0 * t**3 + 3.0 * t**2
    h11 = t**3 - t**2
    
    # Spline interpolation
    blended_val = (val_sub * h00) + \
                  (val_sup * h01) + \
                  (grad_sub * delta_M * h10) + \
                  (grad_sup * delta_M * h11)
                  
    return blended_val

@jax.jit
def transonic_CL_spline(M, M_sub, M_sup, CL_sub, CL_sup):
    """
    Blends CL across transonic region using Prandt-Glauert/Ackeret derivative at M_sub/M_sup:

    CL = CL0 / sqrt(1 - M_sub^2) -> dCL/dM_sub = CL * M_sub / (1 - M_sub^2)
    CL = CL0 / sqrt(M_sup^2 - 1) -> dCL/dM_sup = -CL * M_sup / (M_sup^2 -1)
    """

    grad_sub =  CL_sub * (M_sub / (1.0 - M_sub ** 2))
    grad_sup = -CL_sup * (M_sup / (M_sup ** 2 - 1.0))

    return transonic_spline(M, M_sub, M_sup, CL_sub, CL_sup, grad_sub, grad_sup)

@jax.jit
def peaked_CL_spline(M, M_sub, M_peak, M_sup, val_sub, val_sup, val_peak=0.0, peak_multiplier=1.15):
    """
    Bridges the transonic gap using a two-part Hermite spline to enforce a physical lift peak.
    """
    # 1. Analytical gradients at the far boundaries
    grad_sub = val_sub * (M_sub / (1.0 - M_sub**2))
    grad_sup = -val_sup * (M_sup / (M_sup**2 - 1.0))
    
    # 2. Define the Peak Node (Gradient is explicitly 0.0 at the peak)
    # The peak value is typically 1.1x to 1.2x the subsonic boundary value
    val_peak_sub = val_sub * peak_multiplier
    val_peak = jnp.where(val_peak > 0.0, val_peak, val_peak_sub)
    grad_peak = 0.0 
    
    # --- Helper function for a single Hermite segment ---
    def eval_hermite(m, m0, m1, v0, v1, g0, g1):
        t = (m - m0) / (m1 - m0)
        delta_m = m1 - m0
        h00 = 2.0 * t**3 - 3.0 * t**2 + 1.0
        h10 = t**3 - 2.0 * t**2 + t
        h01 = -2.0 * t**3 + 3.0 * t**2
        h11 = t**3 - t**2
        return (v0 * h00) + (v1 * h01) + (g0 * delta_m * h10) + (g1 * delta_m * h11)

    # 3. Calculate both spline segments
    spline_up = eval_hermite(M, M_sub, M_peak, val_sub, val_peak, grad_sub, grad_peak)
    spline_down = eval_hermite(M, M_peak, M_sup, val_peak, val_sup, grad_peak, grad_sup)
    
    # 4. Blend them perfectly at the peak
    return jnp.where(M <= M_peak, spline_up, spline_down)

@jax.jit
def ensemble_CL_spline(M, M_sub, M_sup, val_sub, val_sup, peak_multiplier=1.15):
    """
    Analytically finds the peak of a wide Hermite spline, boosts it, 
    and bridges the transonic gap using a 3-node spline.
    """
    # 1. Analytical gradients at the wide boundaries
    grad_sub = val_sub * (M_sub / (1.0 - M_sub**2))
    grad_sup = -val_sup * (M_sup / (M_sup**2 - 1.0))
    delta_M_wide = M_sup - M_sub
    
    g0 = grad_sub * delta_M_wide
    g1 = grad_sup * delta_M_wide
    
    # 2. Extract Cubic Coefficients
    a = 2.0 * (val_sub - val_sup) + g0 + g1
    b = 3.0 * (val_sup - val_sub) - 2.0 * g0 - g1
    c = g0
    
    # 3. Analytical Peak Location (Quadratic Formula)
    # The negative root guarantees the local maximum.
    discriminant = jnp.maximum(4.0 * b**2 - 12.0 * a * c, 0.0)
    
    # Protect against a=0 (a pure parabola) to keep AD safe
    t_peak = jnp.where(
        jnp.abs(a) > 1e-8,
        (-2.0 * b - jnp.sqrt(discriminant)) / (6.0 * a),
        -c / (2.0 * b + 1e-8)
    )
    
    # Clip t_peak strictly between 5% and 95% of the transition zone
    # to prevent boundary collapse
    t_peak = jnp.clip(t_peak, 0.05, 0.95)
    
    # Convert t_peak back to physical Mach number
    M_peak = M_sub + t_peak * delta_M_wide

    return peaked_CL_spline(M, M_sub, M_peak, M_sup, val_sub, val_sup, peak_multiplier=peak_multiplier)
    
    # 4. Evaluate the wide spline exactly at t_peak to get our baseline height
    h00_w = 2.0 * t_peak**3 - 3.0 * t_peak**2 + 1.0
    h10_w = t_peak**3 - 2.0 * t_peak**2 + t_peak
    h01_w = -2.0 * t_peak**3 + 3.0 * t_peak**2
    h11_w = t_peak**3 - t_peak**2
    
    base_peak_val = (val_sub * h00_w) + (val_sup * h01_w) + (g0 * h10_w) + (g1 * h11_w)
    
    # 5. Apply the User's Empirical Boost!
    val_peak = base_peak_val * peak_multiplier
    
    return peaked_CL_spline(M, M_sub, M_peak, M_sup,
                            val_sub, val_sup, val_peak=val_peak,
                            peak_multiplier=peak_multiplier)