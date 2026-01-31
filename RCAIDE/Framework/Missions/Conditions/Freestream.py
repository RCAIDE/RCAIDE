# RCAIDE/Framework/Missions/Conditions/Freestream.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
import chex
from dataclasses import field

# package imports
import RNUMPY as rp
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Freestream
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class FreestreamConditions(Conditions):
    """
    Represents the freestream conditions in a flight environment.

    This class encapsulates various atmospheric and flight parameters that define
    the freestream conditions for aerodynamic analysis or simulation.

    Attributes
    ----------
    name : str, optional
        Name of the freestream condition. Default is 'Freestream'.

    speed : rp.ndarray, optional
        speed of the freestream. Default is zeros((1, 1)).
    u : rp.ndarray, optional
        X-component of velocity. Default is zeros((1, 1)).
    v : rp.ndarray, optional
        Y-component of velocity. Default is zeros((1, 1)).
    w : rp.ndarray, optional
        Z-component of velocity. Default is zeros((1, 1)).

    altitude : rp.ndarray, optional
        Altitude of the freestream condition. Default is zeros((1, 1)).

    gravity : rp.ndarray, optional
        Gravitational acceleration. Default is zeros((1, 1)).

    pressure : rp.ndarray, optional
        Atmospheric pressure. Default is zeros((1, 1)).
    temperature : rp.ndarray, optional
        Atmospheric temperature. Default is zeros((1, 1)).
    density : rp.ndarray, optional
        Air density. Default is zeros((1, 1)).

    speed_of_sound : rp.ndarray, optional
        Speed of sound in the atmosphere. Default is zeros((1, 1)).

    dynamic_viscosity : rp.ndarray, optional
        Dynamic viscosity of the air. Default is zeros((1, 1)).
    dynamic_pressure : rp.ndarray, optional
        Dynamic pressure of the freestream. Default is zeros((1, 1)).

    mach_number : rp.ndarray, optional
        Mach number of the freestream. Default is zeros((1, 1)).
    reynolds_number : rp.ndarray, optional
        Reynolds number of the flow. Default is zeros((1, 1)).

    delta_ISA : rp.ndarray, optional
        Deviation from International Standard Atmosphere. Default is zeros((1, 1)).

    Notes
    -----
    All attributes are initialized as zero arrays of shape (1, 1) by default.
    """

    tag:                    str             = 'Freestream'
    atmosphere:             chex.dataclass  = None

    speed:                  rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    u:                      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    v:                      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    w:                      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    altitude:               rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    gravity:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    speed_of_sound:         rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    pressure:               rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    temperature:            rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    density:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    dynamic_viscosity:      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    dynamic_pressure:       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    stagnation_pressure:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    stagnation_temperature: rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    mach_number:            rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    reynolds_number:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    delta_ISA:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    gamma:                  rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    Cp:                     rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    R:                      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestFreestreamConditions(unittest.TestCase):
    def setUp(self):
        self.freestream = FreestreamConditions()

    def test_default_values(self):
        self.assertEqual(self.freestream.tag, 'Freestream')
        np.testing.assert_array_equal(self.freestream.speed, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.u, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.v, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.w, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.altitude, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.gravity, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.pressure, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.temperature, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.density, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.speed_of_sound, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.dynamic_viscosity, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.dynamic_pressure, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.mach_number, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.reynolds_number, rp.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.delta_ISA, rp.zeros((1, 1)))

    def test_custom_name(self):
        custom_freestream = FreestreamConditions(tag="Custom Freestream")
        self.assertEqual(custom_freestream.tag, "Custom Freestream")

    def test_custom_values(self):
        custom_freestream = FreestreamConditions(
            speed=rp.array([[100.0]]),
            altitude=rp.array([[1000.0]]),
            temperature=rp.array([[288.15]]),
            pressure=rp.array([[101325.0]])
        )
        np.testing.assert_array_equal(custom_freestream.speed, rp.array([[100.0]]))
        np.testing.assert_array_equal(custom_freestream.altitude, rp.array([[1000.0]]))
        np.testing.assert_array_equal(custom_freestream.temperature, rp.array([[288.15]]))
        np.testing.assert_array_equal(custom_freestream.pressure, rp.array([[101325.0]]))

    def test_array_shape(self):
        for attr_name in ['speed', 'u', 'v', 'w', 'altitude', 'gravity', 'pressure',
                          'temperature', 'density', 'speed_of_sound', 'dynamic_viscosity',
                          'dynamic_pressure', 'mach_number', 'reynolds_number', 'delta_ISA']:
            with self.subTest(attribute=attr_name):
                attr_value = getattr(self.freestream, attr_name)
                self.assertEqual(attr_value.shape, (1, 1), f"{attr_name} shape is not (1, 1)")


if __name__ == '__main__':
    unittest.main()