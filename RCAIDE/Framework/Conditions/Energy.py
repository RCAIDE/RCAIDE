# RCAIDE/Framework/Conditions/Energy.py
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
from RCAIDE.Framework.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Energy
# ----------------------------------------------------------------------------------------------------------------------

@dataclass(kw_only=True)
class Energy(Conditions):

    #Attribute          Type        Default Value
    total:              np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))
    total_efficiency:   np.ndarray  = field(default_factory=lambda: np.ndarray((1, 1)))