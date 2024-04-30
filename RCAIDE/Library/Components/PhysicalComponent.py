# RCAIDE/Library/Compoments/PhysicalComponent.py
# (c) Copyright 2024 Aerospace Research Community LLC
# 
# Created:  Apr 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Mass_Properties
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class MassProperties:

    mass                : float             = field(init=True, default=0.0)
    volume              : float             = field(init=True, default=0.0)
    density             : float             = field(init=True, default=0.0)
    center_of_gravity   : np.ndarray        = field(init=True,
                                                    default_factory=lambda: np.zeros(3))
    moments_of_inertia  : np.ndarray        = field(init=True,
                                                    default_factory=lambda: np.zeros((3,3)))

    def __post_init__(self):
        if not np.any(self.density):
            if np.any(self.mass) and np.any(self.volume):
                try:
                    self.density = self.mass/self.volume
                except:
                    raise MassPropertiesError("Error in calculating component density. "
                                              "Check mass and volume specification.")


@dataclass
class PhysicalComponent:

    name                : str               = field(init=True)

    origin              : np.ndarray        = field(init=True,
                                                    default_factory=lambda: np.zeros(3))
    mass_properties     : MassProperties    = field(init=True,
                                                    default_factory=MassProperties)

    def sum_mass(self):
        self.mass_properties.mass = 0.

        for k, v in self.__dict__.items():
            if isinstance(v, PhysicalComponent):
                self.mass_properties.mass += v.sum_mass()

    def sum_moments_of_inertia(self):

        self.mass_properties.moments_of_inertia = np.zeros((3, 3))

        for k, v in self.__dict__.items():
            if isinstance(v, PhysicalComponent):
                r = np.linalg.norm(
                    (v.origin + v.mass_properties.center_of_gravity)
                    - self.origin
                )

                self.mass_properties.moments_of_inertia += (
                    v.mass_properties.moments_of_inertia
                    + v.mass_properties.mass * r**2 * np.eye(3)
                )

    def sum_center_of_gravity(self):

        self.mass_properties.center_of_gravity = np.zeros(3)

        for k, v in self.__dict__.items():
            rel_origin = v.origin - self.origin
            rel_cg = rel_origin + v.mass_properties.center_of_gravity

            mass_fraction = v.mass_properties.mass/self.mass_properties.mass
            weighted_cg = rel_cg * mass_fraction

            self.mass_properties.center_of_gravity += weighted_cg

    def add_subcomponent(self, subcomponent: PhysicalComponent):

        eval(f"self.{subcomponent.name} = subcomponent")
        if np.any(subcomponent.mass_properties.mass):
            self.sum_mass()
            if np.any(subcomponent.mass_properties.center_of_gravity):
                self.sum_center_of_gravity()
            if np.any(subcomponent.mass_properties.moments_of_inertia):
                self.sum_moments_of_inertia()

        return None







