# RCAIDE/Framework/Methods/Aerodynamics/initialization.py
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
    from RCAIDE.Framework.System import Aircraft
    from RCAIDE.Framework.Settings import Settings

from RCAIDE.utils import inputs, outputs
from RCAIDE.Framework.Missions.Conditions.Aerodynamics import ComponentCoefficients


# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Aerodynamic Conditions
# ----------------------------------------------------------------------------------------------------------------------

@inputs(
    "system.wings",
    "system.fuselages",
    "system.nacelles"
)
@outputs(
    "state.aerodynamics.coefficients.[ComponentCoefficients].wings",
    "state.aerodynamics.coefficients.[ComponentCoefficients].fuselages",
    "state.aerodynamics.coefficients.[ComponentCoefficients].nacelles"
)
def expand_component_coefficients(
    state: "State",
    system: "Aircraft",
    settings: "Settings"
):

    aero_conditions = state.aerodynamics

    n_wings = len(system.wings)
    n_fuselages = len(system.fuselages)
    n_nacelles = len(system.nacelles)

    def _expand_col(leaf: ComponentCoefficients):
        # 1. Dynamically extract n_time from the already row-expanded arrays
        if isinstance(leaf, ComponentCoefficients):
            n_time = leaf.wings.shape[0]

            # 2. Instantiate the component arrays
            new_wings     = jnp.zeros((n_time, n_wings))
            new_fuselages = jnp.zeros((n_time, n_fuselages))
            new_nacelles  = jnp.zeros((n_time, n_nacelles))

            # 3. Functionally update the leaf
            return eqx.tree_at(
                lambda l: (l.wings, l.fuselages, l.nacelles),
                leaf,
                (new_wings, new_fuselages, new_nacelles)
            )
        else:
            return leaf

    updated_aero = jax.tree_util.tree_map(
        _expand_col,
        aero_conditions,
        is_leaf=lambda leaf: isinstance(leaf, ComponentCoefficients)
    )

    updated_state = eqx.tree_at(lambda s: s.aerodynamics, state, updated_aero)

    return updated_state, system, settings