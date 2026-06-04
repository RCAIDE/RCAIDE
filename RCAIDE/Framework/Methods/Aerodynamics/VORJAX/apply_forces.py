# RCAIDE/Framework/Methods/Aerodynamics/Vortex_Lattice/apply_forces.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Mar 2026, J. Smart
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING

import jax
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  Apply Aerodynamic Forces
# ----------------------------------------------------------------------------------------------------------------------


@inputs(
    "state.aerodynamics.coefficients.lift.total",
    "state.aerodynamics.coefficients.drag.total",
    "state.freestream.density",
    "state.freestream.speed",
    "system.areas.reference",
)
@outputs(
    "state.frames.wind.total_force_vector"
)
def apply_aerodynamic_forces(state: "State", system: "System", settings: "Settings"):
    
    # Get coefficients from analysis
    C_L = state.aerodynamics.coefficients.lift.total
    C_D = state.aerodynamics.coefficients.drag.total

    rho             = state.freestream.density
    flight_speed    = state.freestream.speed
    S               = system.areas.reference
    
    qS = 0.5 * rho * (flight_speed ** 2) * S
    
    F_Z = -qS * C_L # Z negative by right hand rule convention
    F_X = qS * C_D

    wind_forces = state.frames.wind.total_force_vector
    wind_forces = wind_forces.at[:, 2].set(F_Z.flatten())
    wind_forces = wind_forces.at[:, 0].set(F_X.flatten())

    state = eqx.tree_at(lambda s: s.frames.wind.total_force_vector, state, wind_forces)

    return state, system, settings
