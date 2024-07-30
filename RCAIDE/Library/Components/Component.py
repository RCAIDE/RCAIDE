# RCAIDE/Library/Compoments/PhysicalComponent.py
# (c) Copyright 2024 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import TypeVar
from warnings import warn

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Mass_Properties
# ----------------------------------------------------------------------------------------------------------------------


@dataclass
class ComponentRatios:

    effective           : float = 1.0
    nose                : float = 0.0
    tail                : float = 0.0


@dataclass
class ComponentDimensions:

    ordinal_direction   : bool  = field(init=True, default=False)

    reference           : float = field(init=True, default=0.0)
    total               : float = field(init=True, default=0.0)
    maximum             : float = field(init=True, default=0.0)
    effective           : float = field(init=True, default=0.0)

    projected           : float = field(init=True, default=0.0)
    front_projected     : float = field(init=True, default=0.0)
    top_projected       : float = field(init=True, default=0.0)
    side_projected      : float = field(init=True, default=0.0)


@dataclass
class ComponentAreas:

    reference           : float = field(init=True, default=0.0)
    total               : float = field(init=True, default=0.0)
    maximum             : float = field(init=True, default=0.0)
    effective           : float = field(init=True, default=0.0)

    inflow              : float = field(init=True, default=0.0)
    outflow             : float = field(init=True, default=0.0)
    exit                : float = field(init=True, default=0.0)

    projected           : float = field(init=True, default=0.0)
    front_projected     : float = field(init=True, default=0.0)
    top_projected       : float = field(init=True, default=0.0)
    side_projected      : float = field(init=True, default=0.0)

    wetted              : float = field(init=True, default=0.0)
    exposed             : float = field(init=True, default=0.0)


@dataclass
class MassProperties:

    mass                : float             = field(init=True, default=0.0)
    volume              : float             = field(init=True, default=0.0)
    density             : float             = field(init=True, default=0.0)
    center_of_gravity   : np.ndarray        = field(init=True, default_factory=lambda: np.zeros(3))
    moments_of_inertia  : np.ndarray        = field(init=True, default_factory=lambda: np.zeros((3, 3)))

    def __post_init__(self):
        if not np.any(self.density):
            if np.any(self.mass) and np.any(self.volume):
                try:
                    self.density = self.mass/self.volume
                except ValueError:
                    warn("Error in calculating component density. Check mass and volume specifications.")


@dataclass
class MaterialProperties:

    tensile_stress_carrier    : dataclass  = field(init=True, default_factory=dataclass)
    torsional_stress_carrier  : dataclass  = field(init=True, default_factory=dataclass)
    shear_stress_carrier      : dataclass  = field(init=True, default_factory=dataclass)


ComponentType = TypeVar("ComponentType", bound="Component")
SegmentType = TypeVar("SegmentType", bound="ComponentSegment")


@dataclass
class Component:

    #-------------------------------------------------IDENTIFIERS-------------------------------------------------------

    name                : str                   = field(init=True)
    segments            : list[SegmentType]     = field(init=True, default_factory=list)
    origin              : np.ndarray            = field(init=True, default_factory=lambda: np.zeros(3))

    #----------------------------------------------------AREAS----------------------------------------------------------
    areas               : ComponentAreas        = field(init=True, default_factory=ComponentAreas)

    #--------------------------------------------------DIMENSIONS-------------------------------------------------------
    lengths             : ComponentDimensions   = field(init=True, default_factory=ComponentDimensions)
    widths              : ComponentDimensions   = field(init=True, default_factory=ComponentDimensions)
    heights             : ComponentDimensions   = field(init=True, default_factory=ComponentDimensions)

    #-----------------------------------------------MASS & MATERIALS----------------------------------------------------
    mass_properties     : MassProperties        = field(init=True, default_factory=MassProperties)
    material_properties : MaterialProperties    = field(init=True, default_factory=MaterialProperties)

    def sum_mass(self):
        self.mass_properties.mass = 0.

        for k, v in self.__dict__.items():
            if isinstance(v, Component):
                self.mass_properties.mass += v.sum_mass()
            if len(self.segments) > 0:
                self.mass_properties.mass += np.sum([s.mass_properties.mass for s in self.segments])

    def sum_moments_of_inertia(self):

        self.mass_properties.moments_of_inertia = np.zeros((3, 3))

        for k, v in self.__dict__.items():
            if isinstance(v, Component):
                r = np.linalg.norm(
                    (v.origin + v.mass_properties.center_of_gravity)
                    - self.origin
                )

                self.mass_properties.moments_of_inertia += (
                    v.mass_properties.moments_of_inertia
                    + v.mass_properties.mass * r**2 * np.eye(3)
                )

            if len(self.segments) > 0:
                r_seg = np.asarray([np.linalg.norm(s.origin + s.mass_properties.center_of_gravity)-self.origin
                                    for s in self.segments])
                I_seg = np.sum(np.asarray([s.mass_properties.mass for s in self.segments]) * r_seg ** 2) * np.eye(3)
                self.mass_properties.moments_of_inertia += I_seg

    def sum_center_of_gravity(self):

        self.mass_properties.center_of_gravity = np.zeros(3)

        for k, v in self.__dict__.items():
            rel_origin = v.origin - self.origin
            rel_cg = rel_origin + v.mass_properties.center_of_gravity

            mass_fraction = v.mass_properties.mass/self.mass_properties.mass
            weighted_cg = rel_cg * mass_fraction

            self.mass_properties.center_of_gravity += weighted_cg

    def add_subcomponent(self,
                         subcomponent: ComponentType,
                         sum_mass=True,
                         sum_center_of_gravity=True,
                         sum_moments_of_inertia=True
                         ):

        if isinstance(subcomponent, ComponentSegment):

            if subcomponent.segment_index == -1 or subcomponent.segment_index >= len(self.segments):

                subcomponent.segment_index = len(self.segments)
                self.segments.append(subcomponent.segment_index)
            else:
                self.segments.insert(subcomponent.segment_index, subcomponent)

        elif isinstance(subcomponent, Component):
            vars(self)[subcomponent.name] = subcomponent
        else:
            raise TypeError(f"Attempted to add a subcomponent to {self.name} "
                            f"which was not a Component or Component Segment.")

        if sum_mass:
            self.sum_mass()
            if sum_center_of_gravity:
                self.sum_center_of_gravity()
            if sum_moments_of_inertia:
                self.sum_moments_of_inertia()


@dataclass
class ComponentSegment(Component):

    segment_index : int = field(init=True, default=-1)
