# RCAIDE/Framework/Missions/Conditions/Frames.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field

# package imports
import RNUMPY as rp
from RNUMPY.scipy.spatial.transform import Rotation as SP_Rotation

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Frames
# ----------------------------------------------------------------------------------------------------------------------

@chex.dataclass(kw_only=True)
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
        transform_to_inertial : rp.spatial.transform.Rotation
            The rotation that transforms from this frame to the inertial frame.
        total_force_vector : rp.ndarray
            The total force vector acting on the system in this frame.
        total_moment_vector : rp.ndarray
            The total moment vector acting on the frame.
        """

    # Attribute             Type            Default Value
    tag:                    str             = 'Frame'

    transform_to_inertial:  SP_Rotation     = SP_Rotation.from_euler('zyx', [0., 0., 0.])

    total_force_vector:     rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))
    total_moment_vector:    rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))


@chex.dataclass(kw_only=True)
class InertialFrame(Frame):
    """
    A class representing an inertial reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to an inertial frame, such as position, velocity, acceleration, and more.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Inertial Frame'.

    position_vector : rp.ndarray
        The position vector in the inertial frame. Shape (1, 3).

    velocity_vector : rp.ndarray
        The velocity vector in the inertial frame. Shape (1, 3).
    acceleration_vector : rp.ndarray
        The acceleration vector in the inertial frame. Shape (1, 3).

    angular_velocity_vector : rp.ndarray
        The angular velocity vector in the inertial frame. Shape (1, 3).
    angular_acceleration_vector : rp.ndarray
        The angular acceleration vector in the inertial frame. Shape (1, 3).

    gravity_force_vector : rp.ndarray
        The gravity force vector in the inertial frame. Shape (1, 3).
    time : rp.ndarray
        The time array. Shape (1, 1).

    system_range : rp.ndarray
        The range of the system in the inertial frame. Shape (1, 1).
    """

    # Attribute                     Type        Default Value
    tag:                            str         = 'Inertial Frame'

    position_vector:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    velocity_vector:                rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    acceleration_vector:            rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    angular_velocity_vector:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    angular_acceleration_vector:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    gravity_force_vector:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))

    time:                           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    system_range:                   rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class BodyFrame(Frame):
    """
    A class representing a body-fixed reference frame for engineering simulations.

    This class inherits from Frame and provides additional attributes specific
    to a body frame, such as inertial rotations, thrust force vector, and moment vector.

    Attributes
    ----------
    name : str
        The name of the frame. Default is 'Body Frame'.

    inertial_rotations : rp.ndarray
        The rotations of the body frame relative to the inertial frame. Shape (1, 3).

    thrust_force_vector : rp.ndarray
        The thrust force vector in the body frame. Shape (1, 3).

    moment_vector : rp.ndarray
        The moment vector in the body frame. Shape (1, 3).
    """

    # Attribute             Type        Default Value
    tag:                    str         = 'Body Frame'

    inertial_rotations:     rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    thrust_force_vector:    rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))
    moment_vector:          rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 3)))


@chex.dataclass(kw_only=True)
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

    body_rotations : rp.ndarray
        The rotations of the wind frame relative to the body frame. Shape (1, 3).

    transform_to_body : rp.spatial.transform.Rotation
        The rotation that transforms from the wind frame to the body frame.

    velocity_vector : rp.ndarray
        The velocity vector in the wind frame. Shape (1, 3).
    force_vector : rp.ndarray
        The force vector in the wind frame. Shape (1, 3).
    moment_vector : rp.ndarray
        The moment vector in the wind frame. Shape (1, 3).
    """

    # Attribute         Type            Default Value
    tag:               str             = 'Wind Frame'

    body_rotations:     rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))
    transform_to_body:  SP_Rotation     = SP_Rotation.from_euler('zyx', [0., 0., 0.])

    velocity_vector:    rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))
    force_vector:       rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))
    moment_vector:      rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 3)))


@chex.dataclass(kw_only=True)
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

    latitude : rp.ndarray
        The latitude of the system.
    longitude : rp.ndarray
        The longitude of the system.

    true_course : rp.spatial.transform.Rotation
        The rotation representing the true course in the planet frame.
    """

    # Attribute     Type        Default Value
    tag:            str         = 'Planet Frame'
    start_time:     float       = None

    latitude:       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    longitude:      rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    true_course:    SP_Rotation = SP_Rotation.from_euler('zyx', [0., 0., 0.])


@chex.dataclass(kw_only=True)
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
    tag:            str             = 'Dynamic Frames'

    inertial:       InertialFrame   = field(default_factory=lambda: InertialFrame())
    body:           BodyFrame       = field(default_factory=lambda: BodyFrame())
    wind:           WindFrame       = field(default_factory=lambda: WindFrame())
    planet:         PlanetFrame     = field(default_factory=lambda: PlanetFrame())