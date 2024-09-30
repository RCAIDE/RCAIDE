# RCAIDE/Framework/Missions/Conditions/Freestream.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

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

    Parameters
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

    Attributes
    ----------
    Same as parameters.

    Notes
    -----
    All attributes are initialized as zero arrays of shape (1, 1) by default.
    """

    name:               str         = 'Freestream'

    velocity:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
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
