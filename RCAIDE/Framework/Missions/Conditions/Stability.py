# RCAIDE/Framework/Missions/Conditions/Stability.py
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
#  Stability
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class StaticStability(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Static Stability'

    Cm:             np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))
    Cm_alpha:       np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))
    static_margin:  np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))


@dataclass(kw_only=True)
class DynamicStability(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Dynamic Stability'

    pitch_rate:     np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))
    roll_rate:      np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))
    yaw_rate:       np.ndarray  = field(default_factory=lambda: np.ndarray((1,1)))


@dataclass(kw_only=True)
class StabilityConditions(Conditions):

    # Attribute     Type                Default Value
    name:           str                 = 'Stability'

    static:         StaticStability     = StaticStability()
    dynamic:        DynamicStability    = DynamicStability()
