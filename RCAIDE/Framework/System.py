# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports

# ----------------------------------------------------------------------------------------------------------------------
#  System
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MassProperties:

    mass                : float             = field(default=0.0)
    volume              : float             = field(default=0.0)
    density             : float             = field(default=0.0)
    center_of_gravity   : np.ndarray        = field(default_factory=lambda: np.zeros(3))
    moments_of_inertia  : np.ndarray        = field(default_factory=lambda: np.zeros((3, 3)))

    def __post_init__(self):
        if not np.any(self.density):
            if np.any(self.mass) and np.any(self.volume):
                try:
                    self.density = self.mass/self.volume
                except ValueError:
                    warn("Error in calculating component density. Check mass and volume specifications.")


@dataclass(kw_only=True)
class System:

    name: str = 'System'

    mass_properties     : MassProperties        = field(default_factory=MassProperties)

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