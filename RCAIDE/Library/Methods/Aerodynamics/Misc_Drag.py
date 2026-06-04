# RCAIDE/Library/Methods/Aerodynamics/misc_drag.py
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
#  Miscellaneous Drag Components
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# 1. PURE LIBRARY FUNCTION (Math Only)
# ---------------------------------------------------------
@jax.jit
def func_compute_something(array_1, array_2):
    """ Pure JAX mathematical evaluation. """
    
    return jnp.zeros_like(array_1)

# ---------------------------------------------------------
# 2. STATEFUL FRAMEWORK ROUTER
# ---------------------------------------------------------
def compute_something_stateful(state: "State", system: "System", settings: "Settings"):
    """ Unpacks PyTrees, calls pure math, repacks PyTrees. """
    
    # 1. Unpack
    # val = state.aerodynamics.something
    
    # 2. Call pure function
    # result = func_compute_something(val)
    
    # 3. Pack and return
    # current_state = eqx.tree_at(lambda s: s.aerodynamics.result, state, result)
    
    return state, system, settings
