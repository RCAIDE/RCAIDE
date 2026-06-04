# RCAIDE/Framework/Missions/Initialize/state.py
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
#  Initialize/Expand State
# ----------------------------------------------------------------------------------------------------------------------

def expand_state(state: "State", system: "System", settings: "Settings"):
    
    updated_state = state.expand_rows(state.numerics.number_of_control_points)
    
    return updated_state, system, settings
