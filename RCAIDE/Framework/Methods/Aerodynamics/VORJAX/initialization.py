# RCAIDE/Framework/Methods/Aerodynamics/VLM/initialization
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
    
    from RCAIDE.Library.Components.Wings import Wing

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  VLM Initialization
# ----------------------------------------------------------------------------------------------------------------------

@inputs(
    "settings.analysis.aerodynamics: VLMSettings",
    "system.wings.[Wing].chords.mean_aerodynamic",
    "system.wings.[Wing].spans.projected",
    "system.mass_properties.center_of_gravity",
)
@outputs(
    "system.reference_geometry",
    "system.analysis_data"
)
def initialize_VLM_data(state: "State", system: "Aircraft", settings: "Settings"):
    """
    Parses the vehicle geometry to find the primary reference parameters 
    and packs them into JAX arrays for the VLM solver.
    """
    
    if "VLMSettings" not in settings.analysis.aerodynamics.__class__.__name__:
        raise ValueError("settings.analysis.aerodynamics are not VLM Settings."\
        "Please use RCAIDE.Framework.Analysis.Vortex_Lattice.VLMSettings")

    # Standard Python Control Flow (Safe outside of @jax.jit)
    wings = system.wings
    
    ref_wing = None
    if hasattr(wings, 'main_wing'):
        ref_wing = wings.main_wing
    elif len(wings) > 0:
        ref_wing = wings[0]
    
    if ref_wing is not None:
        ref_wing: Wing
        c_bar = ref_wing.chords.mean_aerodynamic
        x_mac = ref_wing.aerodynamic_center[0] + ref_wing.origin[0][0]
        z_mac = ref_wing.aerodynamic_center[2] + ref_wing.origin[0][2]
        b_ref = ref_wing.spans.projected
    else:
        c_bar = 0.0
        x_mac = 0.0
        z_mac = 0.0
        b_ref = 0.0
        
        for wing in wings:
            if not wing.vertical:
                if c_bar <= wing.chords.mean_aerodynamic:
                    c_bar = wing.chords.mean_aerodynamic
                    x_mac = wing.aerodynamic_center[0] + wing.origin[0][0]
                    z_mac = wing.aerodynamic_center[2] + wing.origin[0][2]
                    b_ref = wing.spans.projected

    # 2. Resolve the Center of Gravity / Moment Reference Center
    # Assuming the legacy shape was a 2D array like [[x, y, z]]
    cg_array = system.mass_properties.center_of_gravity
    x_cg = cg_array[0][0]
    z_cg = cg_array[0][2]
    
    x_m = jnp.where(x_cg == 0.0, x_mac, x_cg)
    z_m = jnp.where(x_cg == 0.0, z_mac, z_cg)

    # 3. Pack into strict JAX arrays
    # We use jnp.atleast_1d and explicit array shapes to match your jnp.empty structures
    new_ref_geom = system.reference_geometry.__class__(
        mean_aerodynamic_chord = jnp.atleast_1d(c_bar), #type: ignore
        projected_span         = jnp.atleast_1d(b_ref), #type: ignore
        aerodynamic_center     = jnp.array([[x_mac, 0.0, z_mac]]), #type: ignore
        center_of_gravity      = jnp.array([[x_m,   0.0, z_m]]) #type: ignore
    )

    # Add analysis data keys
    initial_analysis_data = {
            "vortex_distribution": None,
            "VICs": None,
            "induced_wake": None,
            "boundary_conditions": None,
            "relative_velocity": None,
            "singularities": None,
            "vortex_strengths": None,
            "dCp": None,
        }
        
    updated_system = eqx.tree_at(
        lambda s: (s.reference_geometry, s.analysis_data), 
        system, 
        (new_ref_geom, initial_analysis_data)
    )

    return state, updated_system, settings
