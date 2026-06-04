# RCAIDE/Framework/Analyses/Aerodynamics/VLM.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: May 2025, RCAIDE Team
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import warnings

from typing import Callable, Optional, Iterable, Any

# package imports
import equinox as eqx
import jax.numpy as jnp
import sklearn

# RCAIDE imports
from RCAIDE.Library import Units
from RCAIDE.Library.Methods.Aerodynamics.Transonic import transonic_spline, peaked_CL_spline, ensemble_CL_spline

from RCAIDE.Framework import Process, ProcessStep

from RCAIDE.Framework.Methods.Aerodynamics.VORJAX import (check_freestream,
                                                          compute_coefficients, compute_induced_velocity,
                                                          compute_panel_pressures, compute_boundary_conditions,
                                                          compute_vortex_strength,
                                                          initialize_VLM_data, discretize_surfaces,
                                                          apply_aerodynamic_forces)

from RCAIDE.Framework.Methods.Aerodynamics import (expand_component_coefficients,
                                                   compute_parasite_drag,
                                                   compute_viscous_induced_drag)

# ----------------------------------------------------------------------------------------------------------------------
#  VLM Settings
# ----------------------------------------------------------------------------------------------------------------------


class SupersonicSettings(eqx.Module):
    
    begin_blend_mach:               float = 0.5
    end_blend_mach:                 float = 2.0
    
    peak_CL_multiplier:             float = 1.15
    peak_mach_number:               Optional[float] = None
    _transonic_CL_blender:          Callable = eqx.field(static=True, default=ensemble_CL_spline)
    
    begin_drag_rise_mach_number:    float = 0.95
    end_drag_rise_mach_number:      float = 1.2
    
    transonic_drag_multiplier:      float = 1.25
    volume_wave_drag_scaling:       float = 3.2
    
    cross_section_type:             str  = eqx.field(static=True, default='Fixed')
    wave_drag_type:                 str  = eqx.field(static=True, default='Raymer')

    def __post_init__(self):
        if self.peak_mach_number is not None:
            object.__setattr__(self, "_transonic_CL_blender", peaked_CL_spline)
    
    def transonic_CL_blender(self, M, val_sub, val_sup):
        return self._transonic_CL_blender(
            M, 
            self.begin_blend_mach,
            self.peak_mach_number,
            self.end_blend_mach,
            val_sub, val_sup,
            peak_multiplier=self.peak_CL_multiplier
            )

class CorrectionFactors(eqx.Module):

    suction:    bool = eqx.field(static=True, default=True)
    shock:      bool = eqx.field(static=True, default=True)

    fuselage_lift: float = 1.14
    trim_drag: float = 1.02

    viscous_lift_drag: float = 0.38
    lift_to_drag: float = 0.0
    CL_max: float = 1.0


class FormFactors(eqx.Module):

    span_efficiency: float = 1.0
    oswald: float = 1.0

    wing: float = 1.1
    fuselage: float = 2.3
    pylon: float = 0.2


class Surrogate(eqx.Module):

    surrogate:              Optional[Any] = eqx.field(static=True, default_factory=sklearn.gaussian_process.GaussianProcessRegressor)
    
    blend_transonic:        bool          = True

    angle_of_attack:        jnp.ndarray  = eqx.field(default_factory=lambda: jnp.linspace(-5., 15., 40) * Units.deg)
    sideslip_angle:         jnp.ndarray  = eqx.field(default_factory=lambda: jnp.linspace(0.0, 15., 30) * Units.deg)
    Mach:                   jnp.ndarray  = eqx.field(default_factory=lambda: jnp.linspace(0., 0.85, 20))
    
    aileron_deflection:     jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([30, 10.0, 1E-12]) * Units.deg)
    elevator_deflection:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([30, 10.0, 1E-12]) * Units.deg)
    rudder_deflection:      jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([30, 10.0, 1E-12]) * Units.deg)
    flap_deflection:        jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([30, 10.0, 1E-12]) * Units.deg)
    slat_deflection:        jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([30, 10.0, 1E-12]) * Units.deg)

    u:                      jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([0.2, 0.1, 1E-12]))
    v:                      jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([0.2, 0.1, 1E-12]))
    w:                      jnp.ndarray  = eqx.field(default_factory=lambda: jnp.array([0.2, 0.1, 1E-12]))

    pitch_rate:             jnp.ndarray  = eqx.field(default_factory=lambda:jnp.array([0.3, 0.15, 0.0])  * Units.rad / Units.s)
    roll_rate:              jnp.ndarray  = eqx.field(default_factory=lambda:jnp.array([0.3, 0.15, 0.0])  * Units.rad / Units.s)
    yaw_rate:               jnp.ndarray  = eqx.field(default_factory=lambda:jnp.array([0.3, 0.15, 0.0])  * Units.rad / Units.s)

    def fit(self, *args, **kwargs):
        return self.surrogate.fit(*args, **kwargs)
    
    def predict(self, *args, **kwargs):
        return self.surrogate.predict(*args, **kwargs)


class Vortices(eqx.Module):

    model_fuselage:             bool = eqx.field(static=True, default=False)
    verbose:                    bool = eqx.field(static=True, default=False)
    floating_point_precision:   str  = eqx.field(static=True, default="float64")
    
    # Discretization Inputs (Optional, so the user can choose which to define)
    spanwise_cosine:    bool = eqx.field(static=True, default=True)
    chordwise_cosine:   bool = eqx.field(static=True, default=False) # Currently unsupported

    n_spanwise:         Optional[Iterable[int] | int] = eqx.field(static=True, default=8) # Min value is number of wing segments (possibly more for control surfaces)
    n_chordwise:        Optional[Iterable[int] | int] = eqx.field(static=True, default=3) # Min value 3 to allow front and rear control surfaces
    
    # Can set separate values for each wing/fuselage (ex. [8, 4] for [wing, stab] and [4, 2] for [fuselage, nacelle]), else uses global value above
    wings_n_spanwise:   Optional[Iterable[int] | int] = eqx.field(static=True, default=None)
    wings_n_chordwise:  Optional[Iterable[int] | int] = eqx.field(static=True, default=None)

    bodies_n_spanwise:  Optional[Iterable[int] | int] = eqx.field(static=True, default=None)
    bodies_n_chordwise: Optional[Iterable[int] | int] = eqx.field(static=True, default=None)

    def __post_init__(self):
        """Validates discretization inputs and resolves global vs separate routing."""

        if self.chordwise_cosine:
            warnings.warn(f"Chordwise cosine spacing is currently unsupported. Defaulting to linear spacing.")
            object.__setattr__(self, "chordwise_cosine", False)
        
        # Check if the user explicitly provided separate definitions
        separate_provided = any([
            self.wings_n_spanwise is not None,
            self.wings_n_chordwise is not None,
            self.bodies_n_spanwise is not None,
            self.bodies_n_chordwise is not None
        ])

        if separate_provided:
            # Validate that all separate variables were provided
            missing_separate = any(x is None for x in [
                self.wings_n_spanwise, self.wings_n_chordwise,
                self.bodies_n_spanwise, self.bodies_n_chordwise
            ])
            if missing_separate:
                raise ValueError('If using separate surface discretization, all n_sw and n_cw values must be defined.')

        else:
            # User didn't provide separate settings, so we fallback to the global defaults
            if not self.n_spanwise or not self.n_chordwise:
                raise ValueError('If using global surface discretization, both n_sw and n_cw must be defined.')

            # Route the global settings to the specific component fields
            object.__setattr__(self, 'wings_n_spanwise', self.n_spanwise)
            object.__setattr__(self, 'wings_n_chordwise', self.n_chordwise)
            object.__setattr__(self, 'bodies_n_spanwise', self.n_spanwise)
            object.__setattr__(self, 'bodies_n_chordwise', self.n_chordwise)


class VLMSettings(eqx.Module):

    model_fuselage:             bool    = eqx.field(static=True, default=False)
    trim_aircraft:              bool    = eqx.field(static=True, default=False)

    recalculate_wetted_area:    bool    = eqx.field(static=True, default=False)
    model_propeller_wake:       bool    = eqx.field(static=True, default=False)
    near_field_drag:            bool    = eqx.field(static=True, default=False)

    CL_max:                     float   = jnp.inf
    CD_increment:               float   = 0.0
    spoiler_drag_increment:     float   = 0.0

    # Sub-Settings

    vortices:       Vortices                = eqx.field(default_factory=Vortices)

    supersonic:     SupersonicSettings      = eqx.field(default_factory=SupersonicSettings)
    corrections:    CorrectionFactors       = eqx.field(default_factory=CorrectionFactors)
    form_factors:   FormFactors             = eqx.field(default_factory=FormFactors)
    surrogate:      Surrogate               = eqx.field(default_factory=Surrogate)

# ----------------------------------------------------------------------------------------------------------------------
#  VLM Initialization
# ----------------------------------------------------------------------------------------------------------------------

def _default_VORJAX_init_steps():
    return(
        ProcessStep(expand_component_coefficients, "Initialize Component Bookkeeping"),
        ProcessStep(initialize_VLM_data, "Initialize Data Structures"),
        ProcessStep(discretize_surfaces, "Discretize Surfaces"),
    )

class InitializeVORJAX(Process):
    
    tag: str = eqx.field(static=True, default="Initialize VORJAX")
    steps: tuple = eqx.field(default_factory=_default_VORJAX_init_steps)

# ----------------------------------------------------------
#  VLM Process
# ----------------------------------------------------------

def _default_VORJAX_steps():
    return(
        # Lift and Induced Drag
        ProcessStep(check_freestream, "Freestream Validation"),
        ProcessStep(compute_boundary_conditions, "Calculate Boundary Conditions"),
        ProcessStep(compute_induced_velocity, "Calculate VICs"),
        ProcessStep(compute_vortex_strength, "Compute Vortex Strength"),
        ProcessStep(compute_panel_pressures, "Compute Pressure Coefficients"),
        ProcessStep(compute_coefficients, "Compute Aerodynamic Coefficients"),
        ProcessStep(apply_aerodynamic_forces, "Apply Aerodynamic Forces"),

        # Full Drag Buildup
        # ProcessStep(compute_parasite_drag, "Compute Parasite Drag"),
        # ProcessStep(compute_viscous_induced_drag, "Compute Viscous Induced Drag"),
    )
    # TODO: Add trimming/stability analysis

class VORJAX(Process):

    tag: str = eqx.field(static=True, default="Aerodynamics")

    steps : tuple = eqx.field(default_factory=_default_VORJAX_steps)

# ----------------------------------------------------------
#  Surrogate VLM Process
# ----------------------------------------------------------

# TODO: Surrogate VLM initialization, steps, and analysis