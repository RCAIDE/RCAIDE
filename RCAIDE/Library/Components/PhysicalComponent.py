# RCAIDE/Library/Compoments/Mass_Properties.py
# (c) Copyright 2024 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke
# Modified: Apr 2024, J. Smart

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
    center_of_gravity   : np.ndarray        = field(init=True,
                                                    default_factory=lambda: np.zeros(3))
    moments_of_inertia  : np.ndarray        = field(init=True,
                                                    default_factory=lambda: np.zeros((3,3)))

@dataclass
class PhysicalComponent:

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




