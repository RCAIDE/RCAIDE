# RCAIDE/Library/Methods/Aerodynamics/shocks.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: May 2026, J Smart
# Modified: May 2026, J Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING
import jax
import jax.numpy as jnp
from jax.lax import scan

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

# ----------------------------------------------------------------------------------------------------------------------
#  Shock Relations
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# Normal Shock Relations
# ---------------------------------------------------------
@jax.jit
def theta_beta_mach(M0, theta, gamma=1.4, weak_shock=True):
    """
    Computes shock angle (beta) of an oblique shock.
    """
    # Protect against subsonic inputs breaking the arcsin
    M0_safe = jnp.maximum(M0, 1.0 + 1e-8)
    
    # Calculate wave angle
    mu = jnp.arcsin(1.0 / M0_safe)
    c  = jnp.square(jnp.tan(mu))
    
    # Calculate shock angle coefficients
    a = ((gamma - 1.0) / 2.0 + (gamma + 1.0) * c / 2.0) * jnp.tan(theta)
    b = ((gamma + 1.0) / 2.0 + (gamma + 3.0) * c / 2.0) * jnp.tan(theta)
    
    # Protect the square root from negative values if theta > theta_max 
    inner_d = (4.0 * (1.0 - 3.0 * a * b)**3) / jnp.square(27.0 * a**2 * c + 9.0 * a * b - 2.0) - 1.0
    d = jnp.sqrt(jnp.maximum(inner_d, 1e-8))
    
    # Select weak (0) or strong (1) shock root
    n = jnp.where(weak_shock, 0.0, 1.0)
    
    atan_term = jnp.arctan(1.0 / d)
    
    beta = jnp.arctan((b + 9.0 * a * c) / (2.0 * (1.0 - 3.0 * a * b)) - 
                      (d * (27.0 * a**2 * c + 9.0 * a * b - 2.0)) / (6.0 * a * (1.0 - 3.0 * a * b)) * jnp.tan(n * jnp.pi / 3.0 + 1.0 / 3.0 * atan_term))
    
    return beta

@jax.jit
def oblique_shock(M0, theta, beta, gamma=1.4):
    """
    Computes flow quantities/ratios after undergoing an oblique shock.
    """
    # Determine normal component of Mach
    M0_n = M0 * jnp.sin(beta)
    
    # 3. Protect against unphysical subsonic normal components
    M0_n_sq = jnp.maximum(jnp.square(M0_n), 1.0 + 1e-8)
    
    M1_n = jnp.sqrt(((gamma - 1.0) * M0_n_sq + 2.0) / (2.0 * gamma * M0_n_sq - (gamma - 1.0)))
    
    # Determine flow quantities and ratios
    M1  = M1_n / jnp.sin(beta - theta)
    Pr  = (2.0 * gamma * M0_n_sq - (gamma - 1.0)) / (gamma + 1.0)
    Tr  = Pr * (((gamma - 1.0) * M0_n_sq + 2.0) / ((gamma + 1.0) * M0_n_sq))
    
    term1 = ((gamma + 1.0) * M0_n_sq) / ((gamma - 1.0) * M0_n_sq + 2.0)
    term2 = (gamma + 1.0) / (2.0 * gamma * M0_n_sq - (gamma - 1.0))
    Ptr   = (term1 ** (gamma / (gamma - 1.0))) * (term2 ** (1.0 / (gamma - 1.0)))
    
    return M1, Pr, Tr, Ptr

@jax.jit
def normal_shock(M0, gamma=1.4):
    return oblique_shock(M0, theta=0., beta=jnp.pi/2, gamma=gamma)

@jax.jit
def shock_train(M0, thetas, gamma=1.4, weak_shock=True):
    
    def shock_step(carry, theta):
        M0, P0, T0, Pt0= carry
        beta = theta_beta_mach(M0, theta, gamma, weak_shock)
        M1, Pr, Tr, Ptr = oblique_shock(M0, theta, beta, gamma)
        new_carry = (M1, P0 * Pr, T0 * Tr, Pt0 * Ptr)
        return new_carry, None
    
    init_carry = (M0, 1.0, 1.0, 1.0)
    final_carry, _ = scan(shock_step, init_carry, thetas)

    return final_carry  #(Mf, Pr, Tr, Ptr)

if __name__ == '__main__':
    beta = theta_beta_mach(1.5, -jnp.pi/4)
    print(oblique_shock(1.5, -jnp.pi/4, beta))