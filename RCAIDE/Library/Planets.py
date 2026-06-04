# RCAIDE/Library/Planets.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx

from RCAIDE.Library import Units

# ----------------------------------------------------------------------------------------------------------------------
#  Planets
# ----------------------------------------------------------------------------------------------------------------------


class Planet(eqx.Module):

    mass:               float = eqx.field(static=True, default=0.0)
    mean_radius:        float = eqx.field(static=True, default=0.0)
    sea_level_gravity:  float = eqx.field(static=True, default=0.0)

    def compute_gravity(self, altitude: float = 0.0) -> float:

        return self.sea_level_gravity * (self.mean_radius / (self.mean_radius + altitude)) ** 2


class Earth(Planet):

    mass:               float = eqx.field(static=True, default=5.972e24 * Units.kg)
    mean_radius:        float = eqx.field(static=True, default=6371e3 * Units.m)
    sea_level_gravity:  float = eqx.field(static=True, default=9.80665 * Units.parse("m / s**2"))
    HitchHikersGuide:   str   = eqx.field(static=True, default='MostlyHarmless')

    
