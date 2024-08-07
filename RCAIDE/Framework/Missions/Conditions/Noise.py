# RCAIDE/Framework/Missions/Conditions/Noise.py
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
#  Noise
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class NoiseBreakdown(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Noise Breakdown'

    propellers:     np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    lift_rotors:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class NoiseConditions(Conditions):

    # Attribute     Type            Default Value
    name:           str             = 'Noise'

    total:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    breakdown:      NoiseBreakdown = NoiseBreakdown()
