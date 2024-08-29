# RCAIDE/Library/Compoments/PhysicalComponent.py
# (c) Copyright 2024 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Self, TypeVar
from warnings import warn

# package imports 
import numpy as np

# RCAIDE Imports
from RCAIDE.Framework import System

# ----------------------------------------------------------------------------------------------------------------------
#  Mass_Properties
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class ComponentRatios:

    effective:  float   = 1.0
    nose:       float   = 0.0
    tail:       float   = 0.0


@dataclass(kw_only=True)
class ComponentDimensions:

    ordinal_direction   : bool  = field(default=False)

    reference           : float = field(default=0.0)
    total               : float = field(default=0.0)
    maximum             : float = field(default=0.0)
    effective           : float = field(default=0.0)

    projected           : float = field(default=0.0)
    front_projected     : float = field(default=0.0)
    top_projected       : float = field(default=0.0)
    side_projected      : float = field(default=0.0)


@dataclass(kw_only=True)
class ComponentAreas:

    reference           : float = field(default=0.0)
    total               : float = field(default=0.0)
    maximum             : float = field(default=0.0)
    effective           : float = field(default=0.0)

    inflow              : float = field(default=0.0)
    outflow             : float = field(default=0.0)
    exit                : float = field(default=0.0)

    projected           : float = field(default=0.0)
    front_projected     : float = field(default=0.0)
    top_projected       : float = field(default=0.0)
    side_projected      : float = field(default=0.0)

    wetted              : float = field(default=0.0)
    exposed             : float = field(default=0.0)


@dataclass(kw_only=True)
class MaterialProperties:

    tensile_stress_carrier    : dataclass  = field(default_factory=dataclass)
    torsional_stress_carrier  : dataclass  = field(default_factory=dataclass)
    shear_stress_carrier      : dataclass  = field(default_factory=dataclass)


SegmentType = TypeVar("SegmentType", bound="ComponentSegment")


@dataclass(kw_only=True)
class Component:

    # ------------------------------------------------IDENTIFIERS-------------------------------------------------------

    name                : str                   = field(init=True)
    segments            : list[SegmentType]     = field(default_factory=list)
    origin              : np.ndarray            = field(default_factory=lambda: np.zeros(3))

    # ---------------------------------------------------AREAS----------------------------------------------------------
    areas               : ComponentAreas        = field(default_factory=ComponentAreas)

    # -------------------------------------------------DIMENSIONS-------------------------------------------------------
    lengths             : ComponentDimensions   = field(default_factory=ComponentDimensions)
    widths              : ComponentDimensions   = field(default_factory=ComponentDimensions)
    heights             : ComponentDimensions   = field(default_factory=ComponentDimensions)

    # --------------------------------------------------MATERIALS-------------------------------------------------------
    material_properties : MaterialProperties    = field(default_factory=MaterialProperties)


@dataclass(kw_only=True)
class ComponentSegment(Component):

    segment_index : int = field(default=-1)
