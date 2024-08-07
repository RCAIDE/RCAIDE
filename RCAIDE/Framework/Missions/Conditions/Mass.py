# RCAIDE/Framework/Missions/Conditions/Mass.py
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
#  Mass
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MassConditions(Conditions):

    #Attribute          Type        Default Value
    total:              np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    rate_of_change:     np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))

    breakdown:          Conditions  = Conditions(name='Mass Breakdown')
