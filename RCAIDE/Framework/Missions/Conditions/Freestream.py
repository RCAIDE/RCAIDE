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

    #Attribute          Type        Default Value
    name:               str         = 'Freestream'

    velocity:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
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
