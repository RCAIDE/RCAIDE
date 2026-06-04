# RCAIDE/Library/Methods/Aerodynamics/parasite_drag.py
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

from .Flat_Plate import flat_plate_friction

from RCAIDE.utils import inputs, outputs, cubic_spline_blender

# ----------------------------------------------------------------------------------------------------------------------
#  Parasite Drag Methods
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# Wing Parasite Drag
# ---------------------------------------------------------
@jax.jit
def func_wing_parasite_drag(
    Re,
    M,
    T,
    x_tu,
    x_tl,
    w_mac,
    w_sweep,
    w_tc,
    S_ref,
    S_wet,
    form_factor=1.1,
    M_low=0.91,
    M_high=0.99
):
    """Computes the parasite drag due to wings"""  
   
    # Reynolds number
    Re_w = Re * w_mac
    
    cf_w_u, k_comp_u, k_reyn_u = flat_plate_friction(Re_w, M, T, x_tu)
    cf_w_l, k_comp_l, k_reyn_l = flat_plate_friction(Re_w, M, T, x_tl)
    
    # Sweep correciton
    cos_sweep = jnp.cos(w_sweep)
    cos2      = cos_sweep * cos_sweep
    M2        = M * M
    beta2     = jnp.maximum(1.0 - M2 * cos2, 1e-8)
    
    k_w_subsonic = (
        1.0
        + (2.0 * form_factor * (w_tc * cos2)) / jnp.sqrt(beta2)
        + (form_factor * form_factor * cos2 * w_tc * w_tc * (1.0 + 5.0 * cos2)) / (2.0 * beta2)
    )

    k_w_raw = jnp.where(M <= 1.0, k_w_subsonic, 1.0)

    h00_val = cubic_spline_blender(M, M_low, M_high)
    k_w = k_w_raw * h00_val + 1.0 * (1.0 - h00_val)

    # find the final result
    wing_parasite_drag = k_w * cf_w_u * S_wet / S_ref / 2. + k_w * cf_w_l * S_wet / S_ref / 2.

    return wing_parasite_drag, k_w, cf_w_u, cf_w_l, k_comp_u, k_comp_l, k_reyn_u, k_reyn_l

# ---------------------------------------------------------
# Fuselage Parasite Drag
# ---------------------------------------------------------
@jax.jit
def func_tube_fuselage_parasite_drag(
    Re,
    M,
    T,
    S_ref,
    S_wet,
    fuselage_length,
    fuselage_diameter,
    form_factor=2.3,
    M_low=0.91,
    M_high=0.99
):
    """Computes the parasite drag of a tube fuselage."""

    # Transonic form factor effects
    aspect_ratio = fuselage_diameter / fuselage_length

    # Prandtl-Glauert Beta squared (clamped to prevent div-by-zero at Mach 1)
    beta2 = jnp.maximum(1.0 - M ** 2, 1e-8)

    D_sub = jnp.sqrt(1.0 - beta2 * aspect_ratio ** 2)
    a_sub = 2.0 * beta2 * (aspect_ratio ** 2) * (jnp.arctanh(D_sub) - D_sub) / (D_sub ** 3)
    du_sub = a_sub / ((2.0 - a_sub) * jnp.sqrt(beta2))

    D_cap = jnp.sqrt(1.0 - aspect_ratio ** 2)
    a_cap = 2.0 * (aspect_ratio ** 2) * (jnp.arctanh(D_cap) - D_cap) / (D_cap ** 3)
    du_cap = a_cap / (2.0 - a_cap)

    # 3. Blend the two regimes
    h00_val = cubic_spline_blender(M, M_low, M_high)
    du_max_u = du_sub * h00_val + du_cap * (1.0 - h00_val)

    kf = (1.0 + form_factor * du_max_u) ** 2

    # Skin friction coefficient

    Re_l = Re * fuselage_length
    cf, k_comp, k_reyn = flat_plate_friction(Re_l, M, T)

    # Final result
    fuselage_parasite_drag = kf * cf * S_wet / S_ref

    return fuselage_parasite_drag, cf, k_comp, k_reyn

@jax.jit
def func_nacelle_parasite_drag(
    Re,
    M,
    T,
    S_wet,
    S_ref,
    nacelle_length,
    nacelle_diameter,
    pylon_factor=0.2,
    M_low=0.91,
    M_high=0.99,
    has_pylon=True,
):
    """Computes the parasite drag due to a nacelle."""

    Re_l = Re * nacelle_length

    cf, k_comp, k_reyn = flat_plate_friction(Re_l, M, T)
    form_factor = 1 + 0.35 / (nacelle_length / nacelle_diameter)

    h00_val = cubic_spline_blender(M, M_low, M_high)
    C = form_factor * h00_val + (1 - h00_val)

    base_nacelle_parasite_drag = C * cf * S_wet / S_ref

    nacelle_parasite_drag = jnp.where(
        has_pylon,
        base_nacelle_parasite_drag * (1.0 + pylon_factor),
        base_nacelle_parasite_drag
    )

    return nacelle_parasite_drag, cf, k_comp, k_reyn

# ---------------------------------------------------------
# STATEFUL FRAMEWORK ROUTER
# ---------------------------------------------------------


@inputs(
    "settings.analysis.parasite_drag.wing",
    "settings.analysis.aerodynamics.supersonic.begin_blend_mach",
    "settings.analysis.aerodynamics.supersonic.end_blend_mach",
    "settings.analysis.aerodynamics.model_fuselage",
    "state.freestream.reynolds_number",
    "state.freestream.mach_number",
    "state.freestream.temperature",
    "system.wings.[Wing].segments.[WingSegment].chords.mean_aerodynamic",
    "system.wings.[Wing].segments.[WingSegment].sweeps.quarter_chord",
    "system.wings.[Wing].segments.[WingSegment].thickness_to_chord",
    "system.wings.[Wing].segments.[WingSegment].areas.wetted",
    "system.wings.[Wing].transition_x_upper",
    "system.wings.[Wing].transition_x_lower",
    "system.wings.[Wing].chords.mean_aerodynamic",
    "system.wings.[Wing].sweeps.quarter_chord",
    "system.wings.[Wing].thickness_to_chord",
    "system.fuselages.[Fuselage].areas.wetted",
    "system.fuselages.[Fuselage].lengths.total",
    "system.fuselages.[Fuselage].diameters.effective",
    "system.nacelles.[Nacelle].areas.reference",
    "system.nacelles.[Nacelle].lengths.total",
    "system.nacelles.[Nacelle].diameters.maximum"
)
@outputs(
    "state.aerodynamics.coefficients.drag.total",
    "state.aerodynamics.coefficients.drag.parasite.total",
    "state.aerodynamics.coefficients.drag.parasite.wings",
    "state.aerodynamics.coefficients.drag.parasite.fuselages",
    "state.aerodynamics.coefficients.drag.parasite.nacelles",
)
def compute_parasite_drag(state: "State", system: "Aircraft", settings: "Settings"):
    """Computes whole aircraft parasite drag."""

    updated_state = state
    aero_settings = settings.analysis.aerodynamics

    Re = state.freestream.reynolds_number
    M = state.freestream.mach_number
    T = state.freestream.temperature

    # Wing Parasite Drag -----------------------------------
    wing_drags = []

    for wing in system.wings:

        # Check if the wing has defined lifting segments
        if len(wing.segments) > 0:

            # Segment-Level Fidelity Pathway
            seg_macs = jnp.array([seg.chords.mean_aerodynamic for seg in wing.segments])
            seg_sweeps = jnp.array([seg.sweeps.quarter_chord for seg in wing.segments])
            seg_tc = jnp.array([seg.thickness_to_chord for seg in wing.segments])
            seg_swet = jnp.array([seg.areas.wetted for seg in wing.segments])

            # Vectorize the function to process the 1D segment arrays
            vmap_wing_drag = jax.vmap(
                func_wing_parasite_drag,
                in_axes=(None, None, None, None, None, 0, 0, 0, None, 0, None, None, None)
            )

            seg_drags, *_ = vmap_wing_drag(
                Re, M, T,
                wing.transition_x_upper,
                wing.transition_x_lower,
                seg_macs,
                seg_sweeps,
                seg_tc,
                wing.areas.reference,
                seg_swet,
                aero_settings.parasite_drag.wing,
                aero_settings.supersonic.begin_blend_mach,
                aero_settings.supersonic.end_blend_mach
            )

            # Sum the individual segment drags
            wing_drags.append(jnp.sum(seg_drags, axis=0))

        else:
            # Macro/Unsegmented Fidelity Pathway
            drag, *_ = func_wing_parasite_drag(
                Re, M, T,
                wing.transition_x_upper,
                wing.transition_x_lower,
                wing.chords.mean_aerodynamic,
                wing.sweeps.quarter_chord,
                wing.thickness_to_chord,
                system.areas.reference,
                wing.areas.wetted,
                aero_settings.parasite_drag.wing,
                aero_settings.supersonic.begin_blend_mach,
                aero_settings.supersonic.end_blend_mach
            )

            wing_drags.append(drag)

    # Pack the final list into a JAX array
    packed_wings = jnp.column_stack(wing_drags)
    total_wing_parasite_drag = jnp.sum(packed_wings, axis=1)[:, None] if wing_drags else jnp.zeros_like(M)
    
    updated_state = eqx.tree_at(
        lambda s: s.aerodynamics.coefficients.drag.parasite.wings,
        updated_state,
        packed_wings
    )

    if settings.analysis.aerodynamics.model_fuselage:
        # Fuselage Parasite Drag -------------------------------
        fuselage_drags = []
        for fuselage in system.fuselages:
            drag, *_ = func_tube_fuselage_parasite_drag(
                Re, M, T,
                system.areas.reference,
                fuselage.areas.wetted,
                fuselage.lengths.total,
                fuselage.diameters.effective,
                aero_settings.parasite_drag.fuselage,
                aero_settings.supersonic.begin_blend_mach,
                aero_settings.supersonic.end_blend_mach
            )
            fuselage_drags.append(drag)

        packed_fuselages = jnp.column_stack(fuselage_drags)
        total_fuselage_parasite_drag = jnp.sum(packed_fuselages, axis=1)[:, None] if fuselage_drags else jnp.zeros_like(M)

        updated_state = eqx.tree_at(
            lambda s: s.aerodynamics.coefficients.drag.parasite.fuselages,
            updated_state,
            packed_fuselages
        )

        # Nacelle Parasite Drag --------------------------------
        nacelle_drags = []
        for nacelle in system.nacelles:
            drag, *_ = func_nacelle_parasite_drag(
                Re, M, T,
                nacelle.areas.wetted,
                system.areas.reference,
                nacelle.lengths.total,
                nacelle.diameters.maximum,
                aero_settings.parasite_drag.pylon,
                aero_settings.supersonic.begin_blend_mach,
                aero_settings.supersonic.end_blend_mach,
                nacelle.has_pylon
            )
            nacelle_drags.append(drag)

        packed_nacelles = jnp.column_stack(nacelle_drags)
        total_nacelle_parasite_drag = jnp.sum(packed_nacelles, axis=1)[:, None] if nacelle_drags else jnp.zeros_like(M)

        updated_state = eqx.tree_at(
            lambda s: s.aerodynamics.coefficients.drag.parasite.nacelles,
            updated_state,
            packed_nacelles
        )
    else:
        total_fuselage_parasite_drag = jnp.zeros_like(M)
        total_nacelle_parasite_drag = jnp.zeros_like(M)

    # Total Aircraft Parasite Drag
    total_parasite_drag = total_wing_parasite_drag + total_fuselage_parasite_drag + total_nacelle_parasite_drag
    new_total_drag = state.aerodynamics.coefficients.drag.total + total_parasite_drag

    # Update the state tree with the new total drag values
    updated_state = eqx.tree_at(
        lambda s: (s.aerodynamics.coefficients.drag.parasite.total, s.aerodynamics.coefficients.drag.total,),
        updated_state, (total_parasite_drag, new_total_drag)
    )

    return updated_state, system, settings
