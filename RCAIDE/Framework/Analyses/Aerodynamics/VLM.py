# RCAIDE/Framework/Analyses/Aerodynamics/VLM.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field
from typing import Callable

# package imports
import RNUMPY as rp

# RCAIDE imports
import RCAIDE.Framework as rcf
from RCAIDE.Framework.Core import Units

# ----------------------------------------------------------------------------------------------------------------------
#  VLM
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class SupersonicSettings:

    peak_mach_number                        = 1.04
    begin_drag_rise_mach_number             = 0.95
    end_drag_rise_mach_number               = 1.2
    transonic_drag_multiplier               = 1.25
    volume_wave_drag_scaling                = 3.2
    fuselage_parasite_drag_begin_blend_mach = 0.91
    fuselage_parasite_drag_end_blend_mach   = 0.99
    cross_sectional_area_calculation_type   = 'Fixed'
    wave_drag_type                          = 'Raymer'


@chex.dataclass(kw_only=True)
class CorrectionFactors:

    fuselage_lift: float = 1.14
    trim_drag: float = 1.0

    viscous_lift_drag: float = 0.38
    lift_to_drag: float = 0.0
    CL_max: float = 1.0


@chex.dataclass(kw_only=True)
class EfficiencyFactors:

    span: float = None
    oswald: float = None


@chex.dataclass(kw_only=True)
class ParasiteDragFormFactors:

    wing: float = 1.1
    fuselage: float = 2.3


@chex.dataclass(kw_only=True)
class Training:

    angle_of_attack:        rp.ndarray  = None
    Mach:                   rp.ndarray  = None

    sideslip_angle:         rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)
    aileron_deflection:     rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)
    elevator_deflection:    rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)
    rudder_deflection:      rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)
    flap_deflection:        rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)
    slat_deflection:        rp.ndarray  = field(default_factory=lambda: rp.array([30, 10.0, 1E-12]) * Units.deg)

    u:                      rp.ndarray  = field(default_factory=lambda: rp.array([0.2, 0.1, 1E-12]))
    v:                      rp.ndarray  = field(default_factory=lambda: rp.array([0.2, 0.1, 1E-12]))
    w:                      rp.ndarray  = field(default_factory=lambda: rp.array([0.2, 0.1, 1E-12]))

    pitch_rate:             rp.ndarray  = field(default_factory=lambda:rp.array([0.3, 0.15, 0.0])  * Units.rad / Units.sec)
    roll_rate:              rp.ndarray  = field(default_factory=lambda:rp.array([0.3, 0.15, 0.0])  * Units.rad / Units.sec)
    yaw_rate:               rp.ndarray  = field(default_factory=lambda:rp.array([0.3, 0.15, 0.0])  * Units.rad / Units.sec)


@chex.dataclass(kw_only=True)
class Vortices:

    spanwise:   int = 15
    chordwise:  int = 5


@chex.dataclass(kw_only=True)
class VLMSettings:

    discretize_control_surfaces:    bool    = True

    model_fuselage:                 bool    = False
    trim_aircraft:                  bool    = False

    recalculate_total_wetted_area:  bool    = False
    model_propeller_wake:           bool    = False

    CL_max:                         float   = rp.inf
    CD_increment:                   float   = 0.0
    spoiler_drag_increment:         float   = 0.0

    supersonic:     SupersonicSettings      = field(default_factory=SupersonicSettings)
    correction:     CorrectionFactors       = field(default_factory=CorrectionFactors)
    efficiency:     EfficiencyFactors       = field(default_factory=EfficiencyFactors)
    parasite_drag:  ParasiteDragFormFactors = field(default_factory=ParasiteDragFormFactors)
    training:       Training                = field(default_factory=Training)
    vortices:       Vortices                = field(default_factory=Vortices)


@chex.dataclass(kw_only=True)
class VLM(rcf.Process):

    def __post_init__(self):

        if not isinstance(self.settings.analysis.aerodynamics, VLMSettings):
            self.settings.analysis.aerodynamics = VLMSettings()

        self.steps = [
            check_settings,
            inviscid_wings,
            fuselage_correction,
            wing_parasite_drag,
            fuselage_parasite_drag,
            nacelle_parasite_drag,
            pylon_parasite_drag,
            total_parasite_drag,
            induced_drag,
            compressibility_drag,
            miscellaneous_drag,
            spoiler_drag,
            total_drag,
        ]


@chex.dataclass(kw_only=True)
class VLMSurrogate(VLM):

    subsonic:   Callable = None
    transonic:  Callable = None
    supersonic: Callable = None

    def __post_init__(self):
        super().__post_init__()
        self.steps[1] = surrogate_inviscid_wings

    def train_surrogate(self):

        settings = self.settings.analysis.aerodynamics.training

        Mach        = settings.Mach
        alpha       = settings.angle_of_attack
        beta        = settings.sideslip_angle

        u           = settings.u
        v           = settings.v
        w           = settings.w

        pitch_rate  = settings.pitch_rate
        roll_rate   = settings.roll_rate
        yaw_rate    = settings.yaw_rate

        self.system: rcf.Aircraft

        for wing in self.system.wings:
            for control_surface in wing.control_surfaces:
                control_surface.deflection = 0.

        # --------------------------------------------------------------------------------------------------------------
        # AoA Training
        # --------------------------------------------------------------------------------------------------------------

        self.state.initials = rcf.State()
        self.state.initials.freestream.mach_number  = rp.atleast_2d(rp.repeat(Mach, len(alpha))).T
        self.state.aerodynamics.angles.alpha        = rp.atleast_2d(rp.tile(alpha, len(Mach)).T.flatten()).T


