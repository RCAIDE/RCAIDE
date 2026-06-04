# RCAIDE/Compoments/Fuselages/Fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
# package imports
import jax.numpy as jnp
import equinox as eqx

# RCAIDE imports  
from RCAIDE.Library import Component, ComponentDimensions, ComponentFineness, ComponentAreas
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fuselage
# ----------------------------------------------------------------------------------------------------------------------  


class FuselageHeights(ComponentDimensions):

    quarter_length: float                = 0.0
    three_quarters_length: float         = 0.0
    wing_root_quarter_chord: float       = 0.0
    vertical_root_quarter_chord: float   = 0.0

class FuselageLengths(ComponentDimensions):

    nose: float                 = 0.0
    tail: float                 = 0.0
    cabin: float                = 0.0
    fore_space: float           = 0.0
    aft_space: float            = 0.0
    ordinal_direction: bool     = eqx.field(static=True, default=True)

class FuselageSegment(Component):

    percent_x_location: float = 0.0
    percent_z_location: float = 0.0

class Fuselage(Component):

    aerodynamic_center: jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    number_of_seats:        int     = eqx.field(static=True, default=1)
    seats_abreast:          int     = eqx.field(static=True, default=0)
    seat_pitch:             float   = eqx.field(static=True, default=0.0)
    differential_pressure:  float   = eqx.field(static=True, default=0.0)

    heights: ComponentDimensions    = eqx.field(default_factory=FuselageHeights)
    lengths: ComponentDimensions    = eqx.field(default_factory=FuselageLengths)

    diameters:  ComponentDimensions = eqx.field(default_factory=ComponentDimensions)
    fineness:   ComponentFineness   = eqx.field(default_factory=ComponentFineness)

# ---------------------------------------------------------------------------------------------------------------------- 
#  BWB Fuselage
# ----------------------------------------------------------------------------------------------------------------------  

class BWBAreas(ComponentAreas):

    aft_centerbody: float = 0.0

class BWBFuselage(Fuselage):

    tag: str = eqx.field(static=True, default="BWB Fuselage")

    aft_centerbody_taper: float = eqx.field(static=True, default=0.0)

    areas: BWBAreas = eqx.field(default_factory=BWBAreas) # type: ignore
