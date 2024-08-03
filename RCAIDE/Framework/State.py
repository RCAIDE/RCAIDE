# RCAIDE/Framework/Core/State.py
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
from RCAIDE.Framework.Conditions import *

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class State(Conditions):

    #Attribute  Type        Default Value
    name:       str         = 'State'

    numerics:   NumericalConditions    = NumericalConditions()

    initials:   np.ndarray  = field(default_factory=lambda: np.ndarray((1, 0)))
    unknowns:   np.ndarray  = field(default_factory=lambda: np.ndarray((1, 0)))
    residuals:  np.ndarray  = field(default_factory=lambda: np.ndarray((1, 0)))
