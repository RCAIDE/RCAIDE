# RCAIDE/Library/Methods/Aerodynamics/VLM/check_freestream.py
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
#  Check Freestream
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# 1. PURE LIBRARY FUNCTION (Math Only)
# ---------------------------------------------------------
@jax.jit
def func_check_freestream(velocity):
    """ 
    Unpacks and safeguards aerodynamic conditions for the VLM.
    """
    safe_velocity = jnp.where(velocity == 0.0, 1e-6, velocity)
    safe_speed = jnp.linalg.norm(safe_velocity, axis=-1, keepdims=True)
    
    return safe_velocity, safe_speed

# ---------------------------------------------------------
# 2. STATEFUL FRAMEWORK ROUTER
# ---------------------------------------------------------
@inputs(
    "state.frames.inertial.velocity_vector",
)
@outputs(
    "state.frames.inertial.velocity_vector",
    "state.freestream.speed",
)
def check_freestream_stateful(state: "State", system: "System", settings: "Settings"):
    """ Unpacks PyTrees, calls pure math, repacks PyTrees. """
    
    velocity = state.frames.inertial.velocity_vector
    
    safe_velocity, safe_speed = func_check_freestream(velocity)
    
    current_state = eqx.tree_at(lambda s: (s.frames.inertial.velocity_vector, s.freestream.speed), state, (safe_velocity, safe_speed))
    
    return current_state, system, settings
