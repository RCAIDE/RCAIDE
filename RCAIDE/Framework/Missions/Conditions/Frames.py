# RCAIDE/Framework/Missions/Conditions/Frames.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
from dataclasses import dataclass, field

# package imports
import numpy as np
from scipy.spatial.transform import Rotation

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Frames
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Frame(Conditions):
    """
        A base class representing a reference frame for engineering simulations.

        This class inherits from Conditions and provides attributes for frame
        identification, transformation to inertial frame, and total force and
        moment vectors.

        Attributes
        ----------
        name : str
            The name of the frame.
        transform_to_inertial : scipy.spatial.transform.Rotation
            The rotation that transforms from this frame to the inertial frame.
        total_force_vector : np.ndarray
            The total force vector acting on the system in this frame.
        total_moment_vector : np.ndarray
            The total moment vector acting on the frame.
        """

    # Attribute             Type        Default Value
    name:                   str         = 'Frame'

    transform_to_inertial:  Rotation  = Rotation.from_euler('zyx', [0., 0., 0.])

    total_force_vector:     np.ndarray = field(default_factory=lambda: np.zeros((1, 3)))
    total_moment_vector:    np.ndarray = field(default_factory=lambda: np.zeros((1, 3)))


@dataclass(kw_only=True)
class InertialFrame(Frame):
    """
    A class representing an inertial reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to an inertial frame, such as position, velocity, acceleration, and more.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Inertial Frame'.
    position_vector : np.ndarray
        The position vector in the inertial frame. Shape (1, 3).
    velocity_vector : np.ndarray
        The velocity vector in the inertial frame. Shape (1, 3).
    acceleration_vector : np.ndarray
        The acceleration vector in the inertial frame. Shape (1, 3).
    angular_velocity_vector : np.ndarray
        The angular velocity vector in the inertial frame. Shape (1, 3).
    angular_acceleration_vector : np.ndarray
        The angular acceleration vector in the inertial frame. Shape (1, 3).
    gravity_force_vector : np.ndarray
        The gravity force vector in the inertial frame. Shape (1, 3).
    time : np.ndarray
        The time array. Shape (1, 1).
    system_range : np.ndarray
        The range of the system in the inertial frame. Shape (1, 1).
    """

    # Attribute                     Type        Default Value
    name:                           str         = 'Inertial Frame'

    position_vector:                np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    velocity_vector:                np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))
    acceleration_vector:            np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    angular_velocity_vector:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))
    angular_acceleration_vector:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    gravity_force_vector:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    time:                           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    system_range:                   np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class BodyFrame(Frame):
    """
    A class representing a body-fixed reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to a body frame, such as inertial rotations, thrust force vector, and moment vector.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Body Frame'.
    inertial_rotations : np.ndarray
        The rotations of the body frame relative to the inertial frame. Shape (1, 3).
    thrust_force_vector : np.ndarray
        The thrust force vector in the body frame. Shape (1, 3).
    moment_vector : np.ndarray
        The moment vector in the body frame. Shape (1, 3).
    """

    # Attribute             Type        Default Value
    name:                   str         = 'Body Frame'

    inertial_rotations:     np.ndarray  = field(default_factory=lambda: np.ones((1, 3)))

    thrust_force_vector:    np.ndarray  = field(default_factory=lambda: np.ones((1, 3)))

    moment_vector:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))


@dataclass(kw_only=True)
class WindFrame(Frame):
    """
    A class representing a wind reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to a wind frame, such as body rotations, transformation to body frame,
    velocity vector, force vector, and moment vector.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Wind Frame'.
    body_rotations : np.ndarray
        The rotations of the wind frame relative to the body frame. Shape (1, 3).
    transform_to_body : scipy.spatial.transform.Rotation
        The rotation that transforms from the wind frame to the body frame.
    velocity_vector : np.ndarray
        The velocity vector in the wind frame. Shape (1, 3).
    force_vector : np.ndarray
        The force vector in the wind frame. Shape (1, 3).
    moment_vector : np.ndarray
        The moment vector in the wind frame. Shape (1, 3).
    """

    # Attribute         Type        Default Value
    name:               str         = 'Wind Frame'

    body_rotations:     np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))
    transform_to_body:  Rotation    = Rotation.from_euler('zyx', [0., 0., 0.])

    velocity_vector:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    force_vector:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))
    moment_vector:      np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))


@dataclass(kw_only=True)
class PlanetFrame(Frame):
    """
    A class representing a planet-fixed reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to a planet frame, such as start time, latitude, longitude, and true course.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Planet Frame'.
    start_time : float
        The start time of the simulation in the planet frame.
    latitude : np.ndarray
        The latitude of the system.
    longitude : np.ndarray
        The longitude of the system.
    true_course : scipy.spatial.transform.Rotation
        The rotation representing the true course in the planet frame.
    """

    # Attribute         Type        Default Value
    name:               str         = 'Planet Frame'
    start_time:         float       = None

    latitude:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    longitude:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    true_course:        Rotation    = Rotation.from_euler('zyx', [0., 0., 0.])


@dataclass(kw_only=True)
class FrameConditions(Conditions):
    """
    A class representing a collection of reference frames for dynamic simulations.

    This class inherits from Conditions and provides attributes for different
    types of reference frames used in engineering simulations.

    Attributes
    ----------
    name : str
        The name of the frame collection. Default is 'Dynamic Frames'.
    inertial : InertialFrame
        An instance of the InertialFrame class.
    body : BodyFrame
        An instance of the BodyFrame class.
    wind : WindFrame
        An instance of the WindFrame class.
    planet : PlanetFrame
        An instance of the PlanetFrame class.
    """

    # Attribute     Type            Default Value
    name:           str             = 'Dynamic Frames'

    inertial:       InertialFrame   = InertialFrame()
    body:           BodyFrame       = BodyFrame()
    wind:           WindFrame       = WindFrame()
    planet:         PlanetFrame     = PlanetFrame()


class TestFrame(unittest.TestCase):
    def setUp(self):
        self.frame = Frame()

    def test_default_values(self):
        self.assertEqual(self.frame.name, 'Frame')
        np.testing.assert_array_equal(self.frame.total_force_vector, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.frame.total_moment_vector, np.zeros((1, 3)))


class TestInertialFrame(unittest.TestCase):
    def setUp(self):
        self.inertial_frame = InertialFrame()

    def test_default_values(self):
        self.assertEqual(self.inertial_frame.name, 'Inertial Frame')
        np.testing.assert_array_equal(self.inertial_frame.position_vector, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.inertial_frame.velocity_vector, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.inertial_frame.time, np.zeros((1, 1)))


class TestBodyFrame(unittest.TestCase):
    def setUp(self):
        self.body_frame = BodyFrame()

    def test_default_values(self):
        self.assertEqual(self.body_frame.name, 'Body Frame')
        np.testing.assert_array_equal(self.body_frame.inertial_rotations, np.ones((1, 3)))
        np.testing.assert_array_equal(self.body_frame.thrust_force_vector, np.ones((1, 3)))


class TestWindFrame(unittest.TestCase):
    def setUp(self):
        self.wind_frame = WindFrame()

    def test_default_values(self):
        self.assertEqual(self.wind_frame.name, 'Wind Frame')
        np.testing.assert_array_equal(self.wind_frame.body_rotations, np.zeros((1, 3)))
        np.testing.assert_array_equal(self.wind_frame.velocity_vector, np.zeros((1, 3)))


class TestPlanetFrame(unittest.TestCase):
    def setUp(self):
        self.planet_frame = PlanetFrame()

    def test_default_values(self):
        self.assertEqual(self.planet_frame.name, 'Planet Frame')
        self.assertIsNone(self.planet_frame.start_time)
        np.testing.assert_array_equal(self.planet_frame.latitude, np.zeros((1, 1)))
        np.testing.assert_array_equal(self.planet_frame.longitude, np.zeros((1, 1)))


class TestFrameConditions(unittest.TestCase):
    def setUp(self):
        self.frame_conditions = FrameConditions()

    def test_default_values(self):
        self.assertEqual(self.frame_conditions.name, 'Dynamic Frames')
        self.assertIsInstance(self.frame_conditions.inertial, InertialFrame)
        self.assertIsInstance(self.frame_conditions.body, BodyFrame)
        self.assertIsInstance(self.frame_conditions.wind, WindFrame)
        self.assertIsInstance(self.frame_conditions.planet, PlanetFrame)


if __name__ == '__main__':
    unittest.main()

