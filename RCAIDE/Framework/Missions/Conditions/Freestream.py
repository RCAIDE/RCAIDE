# RCAIDE/Framework/Missions/Conditions/Freestream.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Freestream
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class FreestreamConditions(Conditions):
    """
    Represents the freestream conditions in a flight environment.

    This class encapsulates various atmospheric and flight parameters that define
    the freestream conditions for aerodynamic analysis or simulation.

    Attributes
    ----------
    name : str, optional
        Name of the freestream condition. Default is 'Freestream'.

    velocity : np.ndarray, optional
        Velocity (speed) of the freestream. Default is zeros((1, 1)).
    u : np.ndarray, optional
        X-component of velocity. Default is zeros((1, 1)).
    v : np.ndarray, optional
        Y-component of velocity. Default is zeros((1, 1)).
    w : np.ndarray, optional
        Z-component of velocity. Default is zeros((1, 1)).

    altitude : np.ndarray, optional
        Altitude of the freestream condition. Default is zeros((1, 1)).

    gravity : np.ndarray, optional
        Gravitational acceleration. Default is zeros((1, 1)).

    pressure : np.ndarray, optional
        Atmospheric pressure. Default is zeros((1, 1)).
    temperature : np.ndarray, optional
        Atmospheric temperature. Default is zeros((1, 1)).
    density : np.ndarray, optional
        Air density. Default is zeros((1, 1)).

    speed_of_sound : np.ndarray, optional
        Speed of sound in the atmosphere. Default is zeros((1, 1)).

    dynamic_viscosity : np.ndarray, optional
        Dynamic viscosity of the air. Default is zeros((1, 1)).
    dynamic_pressure : np.ndarray, optional
        Dynamic pressure of the freestream. Default is zeros((1, 1)).

    mach_number : np.ndarray, optional
        Mach number of the freestream. Default is zeros((1, 1)).
    reynolds_number : np.ndarray, optional
        Reynolds number of the flow. Default is zeros((1, 1)).

    delta_ISA : np.ndarray, optional
        Deviation from International Standard Atmosphere. Default is zeros((1, 1)).

    Notes
    -----
    All attributes are initialized as zero arrays of shape (1, 1) by default.
    """

    name:               str         = 'Freestream'

    speed:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    u:                  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    v:                  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    w:                  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    altitude:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    gravity:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    pressure:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    temperature:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    density:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    speed_of_sound:     np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    dynamic_viscosity:  np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    dynamic_pressure:   np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    mach_number:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    reynolds_number:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    delta_ISA:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------


class TestFreestreamConditions(unittest.TestCase):
    def setUp(self):
        self.freestream = FreestreamConditions()

    def test_default_values(self):
        self.assertEqual(self.freestream.name, 'Freestream')
        np.testing.assert_array_equal(self.freestream.velocity, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.u, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.v, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.w, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.altitude, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.gravity, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.pressure, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.temperature, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.density, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.speed_of_sound, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.dynamic_viscosity, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.dynamic_pressure, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.mach_number, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.reynolds_number, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.freestream.delta_ISA, np.zeros((1, 1)))

    def test_custom_name(self):
        custom_freestream = FreestreamConditions(name="Custom Freestream")
        self.assertEqual(custom_freestream.name, "Custom Freestream")

    def test_custom_values(self):
        custom_freestream = FreestreamConditions(
            velocity=np.array([[100.0]]),
            altitude=np.array([[1000.0]]),
            temperature=np.array([[288.15]]),
            pressure=np.array([[101325.0]])
        )
        np.testing.assert_array_equal(custom_freestream.velocity, np.array([[100.0]]))
        np.testing.assert_array_equal(custom_freestream.altitude, np.array([[1000.0]]))
        np.testing.assert_array_equal(custom_freestream.temperature, np.array([[288.15]]))
        np.testing.assert_array_equal(custom_freestream.pressure, np.array([[101325.0]]))

    def test_array_shape(self):
        for attr_name in ['velocity', 'u', 'v', 'w', 'altitude', 'gravity', 'pressure',
                          'temperature', 'density', 'speed_of_sound', 'dynamic_viscosity',
                          'dynamic_pressure', 'mach_number', 'reynolds_number', 'delta_ISA']:
            with self.subTest(attribute=attr_name):
                attr_value = getattr(self.freestream, attr_name)
                self.assertEqual(attr_value.shape, (1, 1), f"{attr_name} shape is not (1, 1)")


if __name__ == '__main__':
    unittest.main()