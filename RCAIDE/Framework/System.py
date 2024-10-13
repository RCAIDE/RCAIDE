# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from warnings import warn
from typing import TypeVar, List

# package imports
import numpy as np

# RCAIDE imports

ComponentType = TypeVar("ComponentType", bound="Component")

# ----------------------------------------------------------------------------------------------------------------------
# Components
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class ComponentRatios:

    # Attribute     Type    Default Value
    effective:      float   = 1.0
    nose:           float   = 0.0
    tail:           float   = 0.0


@dataclass(kw_only=True)
class ComponentDimensions:

    # Attribute         Type    Default Value
    ordinal_direction:  bool    = field(default=False)

    reference:          float   = field(default=0.0)
    total:              float   = field(default=0.0)
    maximum:            float   = field(default=0.0)
    effective:          float   = field(default=0.0)

    projected:          float   = field(default=0.0)
    front_projected:    float   = field(default=0.0)
    top_projected:      float   = field(default=0.0)
    side_projected:     float   = field(default=0.0)


@dataclass(kw_only=True)
class ComponentAreas:

    # Attribute         Type    Default Value
    reference:          float   = field(default=0.0)
    total:              float   = field(default=0.0)
    maximum:            float   = field(default=0.0)
    effective:          float   = field(default=0.0)

    inflow:             float   = field(default=0.0)
    outflow:            float   = field(default=0.0)
    exit:               float   = field(default=0.0)

    projected:          float   = field(default=0.0)
    front_projected:    float   = field(default=0.0)
    top_projected:      float   = field(default=0.0)
    side_projected:     float   = field(default=0.0)

    wetted:             float   = field(default=0.0)
    exposed:            float   = field(default=0.0)


@dataclass(kw_only=True)
class MaterialProperties:

    # Attribute                 Type        Default Value
    tensile_stress_carrier:     dataclass   = field(default_factory=dataclass)
    torsional_stress_carrier:   dataclass   = field(default_factory=dataclass)
    shear_stress_carrier:       dataclass   = field(default_factory=dataclass)


@dataclass(kw_only=True)
class MassProperties:

    # Attribute                         Type        Default Value
    total:                              float       = field(default=0.0)
    subcomponent_total:                 float       = field(default=0.0)

    volume:                             float       = field(default=1.0)
    density:                            float       = field(default=0.0)

    center_of_gravity:                  np.ndarray  = field(default_factory=lambda: np.zeros(3))
    moments_of_inertia:                 np.ndarray  = field(default_factory=lambda: np.zeros((3, 3)))
    subcomponent_moments_of_inertia:    np.ndarray  = field(default_factory=lambda: np.zeros((3, 3)))

    def __post_init__(self):
        if not np.any(self.density):
            if np.any(self.total) and np.any(self.volume):
                try:
                    self.density = self.total / self.volume
                except ValueError:
                    warn("Error in calculating component density. Check mass and volume specifications.")


@dataclass(kw_only=True)
class Component:

    # ------------------------------------------------IDENTIFIERS-------------------------------------------------------

    name:                   str                   = 'Component'
    segments:               List[ComponentType]   = field(default_factory=list)
    origin:                 np.ndarray            = field(default_factory=lambda: np.zeros(3))

    # ---------------------------------------------------AREAS----------------------------------------------------------
    areas:                  ComponentAreas        = field(default_factory=ComponentAreas)

    # -------------------------------------------------DIMENSIONS-------------------------------------------------------
    lengths:                ComponentDimensions   = field(default_factory=ComponentDimensions)
    widths:                 ComponentDimensions   = field(default_factory=ComponentDimensions)
    heights:                ComponentDimensions   = field(default_factory=ComponentDimensions)

    # -----------------------------------------------MASS & MATERIALS---------------------------------------------------
    mass_properties:        MassProperties        = field(default_factory=MassProperties)
    material_properties:    MaterialProperties    = field(default_factory=MaterialProperties)

    def add_segment(self, segment: ComponentType, index: int = -1):
        self.segments.insert(index, segment)


# ----------------------------------------------------------------------------------------------------------------------
#  System
# ----------------------------------------------------------------------------------------------------------------------

@dataclass(kw_only=True)
class System(Component):

    name: str = 'System'
    subcomponents: List[Component] = field(default_factory=list)

    def sum_mass(self):

        self.mass_properties.subcomponent_total = np.sum([c.mass_properties.total for c in self.subcomponents])

    def sum_moments_of_inertia(self):

        raise NotImplementedError("Subcomponent moments of inertia calculation is not implemented for the System class.")

    def sum_center_of_gravity(self):

        self.mass_properties.center_of_gravity = np.zeros(3)

        for sc in self.subcomponents:
            rel_origin = sc.origin - self.origin
            rel_cg = rel_origin + sc.mass_properties.center_of_gravity

            mass_fraction = sc.mass_properties.total / self.mass_properties.total
            weighted_cg = rel_cg * mass_fraction

            self.mass_properties.center_of_gravity += weighted_cg

    def add_subcomponent(self,
                         subcomponent: Component,
                         sum_mass=True,
                         sum_center_of_gravity=True,
                         sum_moments_of_inertia=False
                         ):

        if isinstance(subcomponent, Component):
            vars(self)[subcomponent.name] = subcomponent
            self.subcomponents.append(subcomponent)
        else:
            raise TypeError(f"Attempted to add a subcomponent to {self.name} "
                            f"which was not a Component datastructure.")

        if sum_mass:
            self.sum_mass()
            if sum_center_of_gravity:
                self.sum_center_of_gravity()
            if sum_moments_of_inertia:
                self.sum_moments_of_inertia()


if __name__ == '__main__':
    B737 = System(name='Boeing 737')
    print(B737)
