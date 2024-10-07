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

# ----------------------------------------------------------------------------------------------------------------------
# Components
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class ComponentRatios:

    effective:  float   = 1.0
    nose:       float   = 0.0
    tail:       float   = 0.0


@dataclass(kw_only=True)
class ComponentDimensions:

    ordinal_direction: bool  = field(default=False)

    reference: float = field(default=0.0)
    total: float = field(default=0.0)
    maximum: float = field(default=0.0)
    effective: float = field(default=0.0)

    projected: float = field(default=0.0)
    front_projected: float = field(default=0.0)
    top_projected: float = field(default=0.0)
    side_projected: float = field(default=0.0)


@dataclass(kw_only=True)
class ComponentAreas:

    reference: float = field(default=0.0)
    total: float = field(default=0.0)
    maximum: float = field(default=0.0)
    effective: float = field(default=0.0)

    inflow: float = field(default=0.0)
    outflow: float = field(default=0.0)
    exit: float = field(default=0.0)

    projected: float = field(default=0.0)
    front_projected: float = field(default=0.0)
    top_projected: float = field(default=0.0)
    side_projected: float = field(default=0.0)

    wetted: float = field(default=0.0)
    exposed: float = field(default=0.0)


@dataclass(kw_only=True)
class MaterialProperties:

    tensile_stress_carrier: dataclass  = field(default_factory=dataclass)
    torsional_stress_carrier: dataclass  = field(default_factory=dataclass)
    shear_stress_carrier: dataclass  = field(default_factory=dataclass)


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


ComponentType = TypeVar("ComponentType", bound="Component")


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

        # def _subcomponent_MOI(c: Component) -> np.ndarray:
        #     r = np.linalg.norm((c.origin + c.mass_properties.center_of_gravity) - self.origin)
        #     sc_MOI = c.mass_properties.moments_of_inertia + c.mass_properties.total * r ** 2 * np.eye(3)
        #     return sc_MOI
        #
        # self.mass_properties.subcomponent_moments_of_inertia = [self.sum_moments_of_inertia._subcomponent_MOI(c) for c in self.subcomponents]

        # for k, v in vars(self):
        #     if isinstance(v, Component):
        #         self.mass_properties.moments_of_inertia += (
        #                 v.mass_properties.moments_of_inertia
        #                 + v.mass_properties.total * r ** 2 * np.eye(3)
        #         )
        #
        #     if len(self.segments) > 0:
        #         r_seg = np.asarray([np.linalg.norm(s.origin + s.mass_properties.center_of_gravity)-self.origin
        #                             for s in self.segments])
        #         I_seg = np.sum(np.asarray([s.mass_properties.total for s in self.segments]) * r_seg ** 2) * np.eye(3)
        #         self.mass_properties.moments_of_inertia += I_seg
        #
        # for k, v in vars(self).items():
        #     if isinstance(v, Component):
        #
        #
        #         self.mass_properties.moments_of_inertia += (
        #                 v.mass_properties.moments_of_inertia
        #                 + v.mass_properties.total * r ** 2 * np.eye(3)
        #         )
        #
        #     if len(self.segments) > 0:
        #         r_seg = np.asarray([np.linalg.norm(s.origin + s.mass_properties.center_of_gravity)-self.origin
        #                             for s in self.segments])
        #         I_seg = np.sum(np.asarray([s.mass_properties.total for s in self.segments]) * r_seg ** 2) * np.eye(3)
        #         self.mass_properties.moments_of_inertia += I_seg

    def sum_center_of_gravity(self):

        self.mass_properties.center_of_gravity = np.zeros(3)

        for k, v in vars(self).items():
            rel_origin = v.origin - self.origin
            rel_cg = rel_origin + v.mass_properties.center_of_gravity

            mass_fraction = v.mass_properties.total / self.mass_properties.total
            weighted_cg = rel_cg * mass_fraction

            self.mass_properties.center_of_gravity += weighted_cg

    def add_subcomponent(self,
                         subcomponent: Component,
                         sum_mass=True,
                         sum_center_of_gravity=True,
                         sum_moments_of_inertia=True
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
