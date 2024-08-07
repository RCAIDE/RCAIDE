# RCAIDE/Framework/Missions/Conditions/Frames.py
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
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Frames
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Frame(Conditions):

    #Attribute              Type        Default Value
    name:                   str         = 'Frame'

    transform_to_inertial:  np.ndarray  = field(default_factory=lambda: np.ndarray((0, 0, 0)))


@dataclass(kw_only=True)
class InertialFrame(Frame):

    #Attribute      Type        Default Value
    name:           str         = 'Inertial Frame'

    position:       np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))
    velocity:       np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))
    acceleration:   np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))

    gravity_force:  np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))
    total_force:    np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))

    time:           np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    system_range:   np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))


@dataclass(kw_only=True)
class BodyFrame(Frame):

    #Attribute              Type        Default Value
    name:                   str         = 'Body Frame'

    inertial_rotations:     np.ndarray  = field(default_factory=lambda: np.ones((1, 3)))

    thrust_force:           np.ndarray  = field(default_factory=lambda: np.ones((1, 3)))


@dataclass(kw_only=True)
class WindFrame(Frame):

    #Attribute      Type        Default Value
    name:           str         = 'Wind Frame'

    body_rotations: np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))

    velocity:       np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))

    lift_force:     np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))
    drag_force:     np.ndarray  = field(default_factory=lambda: np.ndarray((1, 3)))


@dataclass(kw_only=True)
class PlanetFrame(Frame):

    name:       str = 'Planet Frame'
    start_time: float = None

    latitude:   np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))
    longitude:  np.ndarray = field(default_factory=lambda: np.ndarray((1, 1)))


@dataclass(kw_only=True)
class FrameConditions(Conditions):

    #Attribute  Type            Default Value
    name:       str             = 'Dynamic Frames'

    inertial:   InertialFrame   = InertialFrame()
    body:       BodyFrame       = BodyFrame()
    wind:       WindFrame       = WindFrame()
    planet:     PlanetFrame     = PlanetFrame()

