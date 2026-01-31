# RCAIDE/Compoments/Fuselages/Fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
import RNUMPY as rp
import chex
from dataclasses import field

# RCAIDE imports  
import RCAIDE.Library as rcl
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fuselage
# ----------------------------------------------------------------------------------------------------------------------  


@chex.dataclass(kw_only=True)
class FuselageHeights(rcl.ComponentDimensions):

    at_quarter_length: float                = 0.0
    at_three_quarters_length: float         = 0.0
    at_wing_root_quarter_chord: float       = 0.0
    at_vertical_root_quarter_chord: float   = 0.0


@chex.dataclass(kw_only=True)
class FuselageLengths(rcl.ComponentDimensions):

    nose: float         = 0.0
    tail: float         = 0.0
    cabin: float        = 0.0
    fore_space: float   = 0.0
    aft_space: float    = 0.0


@chex.dataclass(kw_only=True)
class FuselageSegment(rcl.Component):

    percent_x_location: float = 0.0
    percent_z_location: float = 0.0


@chex.dataclass(kw_only=True)
class Fuselage(rcl.Component):

    aerodynamic_center: rp.ndarray = field(default_factory=lambda: rp.zeros(3))

    number_of_seats:        int   = 1
    seats_abreast:          int   = 0.0
    seat_pitch:             float = 0.0
    differential_pressure:  float = 0.0

    heights: FuselageHeights = field(default_factory=FuselageHeights)
    lengths: FuselageLengths = field(default_factory=FuselageLengths)

    diameters: rcl.ComponentDimensions  = field(default_factory=rcl.ComponentDimensions)
    fineness: rcl.ComponentFineness     = field(default_factory=rcl.ComponentFineness)

    def __post_init__(self):
        self.lengths.ordinal_direction = True


@chex.dataclass(kw_only=True)
class BWBFuselage(Fuselage):

    aft_centerbody_taper: float = 0.0

    def __post_init__(self):

        self.areas.aft_centerbody = 0.0
