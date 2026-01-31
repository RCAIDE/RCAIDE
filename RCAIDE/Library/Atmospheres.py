# RCAIDE/Library/Atmospheres.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: May 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field

# package imports
import RNUMPY as rp

# RCAIDE imports
import RCAIDE.Library as rcl

# ----------------------------------------------------------------------------------------------------------------------
#  Atmospheres
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class AtmosphericBreakpoints:

    altitude: rp.ndarray = None
    temperature: rp.ndarray = None
    pressure: rp.ndarray = None
    density: rp.ndarray = None


@chex.dataclass(kw_only=True)
class Atmosphere:

    fluid: rcl.Gases.Gas = field(default_factory=rcl.Gases.Air)

    planet: rcl.Planets.Planet = field(default_factory=rcl.Planets.Earth)

    breaks: AtmosphericBreakpoints = field(default_factory=AtmosphericBreakpoints)


@chex.dataclass(kw_only=True)
class USStandard1976(Atmosphere):

    def __post_init__(self):
        self.breaks.altitude    = rp.array([-2.e3,     0.0e3,    11.e3,      20.e3,      32.e3,      47.e3,      51.e3,      71.e3,      84.852e3])  # m
        self.breaks.temperature = rp.array([301.15,    288.15,   216.65,     216.65,     228.65,     270.65,     270.65,     214.65,     186.95])  # K
        self.breaks.pressure    = rp.array([127774.0,  101325.0, 22632.1,    5474.89,    868.019,    110.906,    66.9389,    3.95642,    0.3734])  # Pa
        self.breaks.density     = rp.array([1.47808e0, 1.2250e0, 3.63918e-1, 8.80349e-2, 1.32250e-2, 1.42753e-3, 8.61606e-4, 6.42099e-5, 6.95792e-6])  # kg/m^3


@chex.dataclass(kw_only=True)
class ConstantTemperature(Atmosphere):

    def __post_init__(self):
        self.breaks.altitude    = rp.array([-2.e3,     0.0e3,     11.e3,    20.e3,     32.e3,     47.e3,      51.e3,      71.e3,       84.852e3])  # m
        self.breaks.temperature = rp.array([301.15,    301.15,    301.15,   301.15,    301.15,    301.15,     301.15,     301.15,      301.15])      # K
        self.breaks.pressure    = rp.array([127774.0,  101325.0,  22632.1,  5474.89,   868.019,   110.906,    66.9389,    3.95642,     0.3734])  # Pa
        self.breaks.density     = rp.array([1.545586,  1.2256523, 0.273764,	0.0662256, 0.0105000, 1.3415E-03, 8.0971E-04, 4.78579E-05, 4.51674E-06]) #kg/m^3