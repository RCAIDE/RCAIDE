# RCAIDE/Library/Methods/Aerodynamics/flat_plate_drag.py
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

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD DESCRIPTION
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# 1. PURE LIBRARY FUNCTION (Math Only)
# ---------------------------------------------------------
@jax.jit
def func_compressible_mixed_flat_plate(Re, M, T, x_t):
    """Calculates coefficient of friction for a flat plate with given turbulent
    transition point, x_t.
    """
    
    x_t = jnp.clip(x_t, 0.0, 1.0)

    Rex = jnp.maximum(Re * x_t, 1.01)

    theta  = 0.671 * x_t / (Rex**0.5)
    x_eff  = (27.78 * theta * Re**0.2)**1.25
    Rext   = jnp.maximum(Re * (1 - x_t + x_eff), 1.01)
    
    cf_turb  = 0.455 / (jnp.log10(Rext)**2.58)
    cf_lam   = 1.328 / (Rex**0.5)

    safe_re_xeff = jnp.maximum(Re * x_eff, 1.01)

    cf_start = jnp.where(
        x_t > 0.0,
        0.455 / (jnp.log10(safe_re_xeff)**2.58),
        0.0
    )
    
    cf_inc = cf_lam * x_t + cf_turb * (1 - x_t + x_eff) - cf_start * x_eff
    
    # Compressibility correction
    Tw = T * (1. + 0.178 * M * M)
    Td = T * (1. + 0.035 * M * M + 0.45 * (Tw / T - 1.))
    k_comp = (T / Td) 
    
    # Reynolds correction
    Rd_w   = Re * (Td / T)**1.5 * ((Td + 216.) / (T + 216.))
    k_reyn = (Re / Rd_w)**0.2
    
    # Calculate coefficient of friction
    cf_comp = cf_inc * k_comp * k_reyn
    
    return cf_comp, k_comp, k_reyn


@jax.jit
def func_compressible_turbulent_flat_plate(Re, M, T):
    """Calculates coefficient of fricton for a fully turbulent flat plate.
    """     

    Re = jnp.maximum(Re, 1.01)

    # Incompressible skin friction coefficient
    cf_inc = 0.455 / (jnp.log10(Re))**2.58
    
    # Compressibility correction
    Tw = T * (1. + 0.178 * M**2.)
    Td = T * (1. + 0.035 * M**2. + 0.45 * (Tw / T - 1.))
    k_comp = T / Td 
    
    # Reynolds correction
    Rd_w   = Re * (Td / T)**1.5 * ((Td + 216.) / (T + 216.))
    k_reyn = (Re / Rd_w)**0.2
    
    # Calculate coefficient of friction
    cf_comp = cf_inc * k_comp * k_reyn
    
    return cf_comp, k_comp, k_reyn


@jax.jit
def flat_plate_friction(Re_w, M, T, x_t=0.0):
    """
    Safely routes to turbulent or mixed flat plate physics,
    guaranteeing NaN-free evaluation across all branches.
    """

    # 1. Pure turbulent calculation (always safe)
    cf_turb, k_comp_turb, k_reyn_turb = func_compressible_turbulent_flat_plate(Re_w, M, T)

    # 2. Protect the mixed calculation from seeing dangerous 0.0 values!
    # If x_t is < 0.01, we artificially feed the mixed function 0.01
    # so it calculates safely and avoids NaN singularities.
    safe_x_t = jnp.maximum(x_t, 0.01)
    cf_mixed, k_comp_mixed, k_reyn_mixed = func_compressible_mixed_flat_plate(Re_w, M, T, safe_x_t)

    # 3. Select the correct outputs based on the true x_t
    is_fully_turbulent = x_t < 0.01

    cf_final = jnp.where(is_fully_turbulent, cf_turb, cf_mixed)
    k_comp_final = jnp.where(is_fully_turbulent, k_comp_turb, k_comp_mixed)
    k_reyn_final = jnp.where(is_fully_turbulent, k_reyn_turb, k_reyn_mixed)

    return cf_final, k_comp_final, k_reyn_final